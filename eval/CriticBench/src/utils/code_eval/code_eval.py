# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The CodeEval metric estimates the pass@k metric for code synthesis.
This is an evaluation harness for the HumanEval problem solving dataset
described in the paper "Evaluating Large Language Models Trained on Code"
(https://arxiv.org/abs/2107.03374)."""

import itertools
import os
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import ipdb

from .execute import check_correctness


def find_first_function_name(string):
    if string.startswith('check'):
        string = string.replace('check(', '').replace(')', '')
        return string
    try:
        function_names = []
        for substring in string.split('\n'):
            if not (substring.startswith('def') is True or substring.startswith('assert') is True):
                continue
            index = substring.index('def ')
            function_name = substring[index:].split('\n')[0]
            f_index = function_name.index('(')
            function_name = function_name[:f_index].replace('def', '').strip()
            function_names.append(function_name)
    except:
        function_names = []
        for substring in string.split('\n'):
            if not (substring.startswith('def') is True or substring.startswith('assert') is True):
                continue
            index = string.index('assert ')
            function_name = string[index:].split('\n')[0]
            f_index = function_name.index('(')
            function_name = function_name[:f_index].replace('assert', '').strip()
            function_names.append(function_name)
    assert len(function_names) > 0
    return function_names[-1]


_CITATION = """\
@misc{chen2021evaluating,
      title={Evaluating Large Language Models Trained on Code},
      author={Mark Chen and Jerry Tworek and Heewoo Jun and Qiming Yuan \
and Henrique Ponde de Oliveira Pinto and Jared Kaplan and Harri Edwards \
and Yuri Burda and Nicholas Joseph and Greg Brockman and Alex Ray \
and Raul Puri and Gretchen Krueger and Michael Petrov and Heidy Khlaaf \
and Girish Sastry and Pamela Mishkin and Brooke Chan and Scott Gray \
and Nick Ryder and Mikhail Pavlov and Alethea Power and Lukasz Kaiser \
and Mohammad Bavarian and Clemens Winter and Philippe Tillet \
and Felipe Petroski Such and Dave Cummings and Matthias Plappert \
and Fotios Chantzis and Elizabeth Barnes and Ariel Herbert-Voss \
and William Hebgen Guss and Alex Nichol and Alex Paino and Nikolas Tezak \
and Jie Tang and Igor Babuschkin and Suchir Balaji and Shantanu Jain \
and William Saunders and Christopher Hesse and Andrew N. Carr \
and Jan Leike and Josh Achiam and Vedant Misra and Evan Morikawa \
and Alec Radford and Matthew Knight and Miles Brundage and Mira Murati \
and Katie Mayer and Peter Welinder and Bob McGrew and Dario Amodei \
and Sam McCandlish and Ilya Sutskever and Wojciech Zaremba},
      year={2021},
      eprint={2107.03374},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
"""

_DESCRIPTION = """\
This metric implements the evaluation harness for the HumanEval problem solving dataset
described in the paper "Evaluating Large Language Models Trained on Code"
(https://arxiv.org/abs/2107.03374).
"""


_KWARGS_DESCRIPTION = """
Calculates how good are predictions given some references, using certain scores
Args:
    predictions: list of candidates to evaluate. Each candidates should be a list
        of strings with several code candidates to solve the problem.
    references: a list with a test for each prediction. Each test should evaluate the
        correctness of a code candidate.
    k: number of code candidates to consider in the evaluation (Default: [1, 10, 100])
    num_workers: number of workers used to evaluate the canidate programs (Default: 4).
    timeout:
Returns:
    pass_at_k: dict with pass rates for each k
    results: dict with granular results of each unittest
Examples:
    >>> test_cases = ["assert add(2,3)==5"]
    >>> candidates = [["def add(a,b): return a*b", "def add(a, b): return a+b"]]
    >>> pass_at_k, results = compute_code_eval(references=test_cases, predictions=candidates, k=[1, 2])
    >>> print(pass_at_k)
    {'pass@1': 0.5, 'pass@2': 1.0}
"""


_WARNING = """
################################################################################
                                  !!!WARNING!!!
################################################################################
The "code_eval" metric executes untrusted model-generated code in Python.
Although it is highly unlikely that model-generated code will do something
overtly malicious in response to this test suite, model-generated code may act
destructively due to a lack of model capability or alignment.
Users are strongly encouraged to sandbox this evaluation suite so that it
does not perform destructive actions on their host or network. For more
information on how OpenAI sandboxes its code, see the paper "Evaluating Large
Language Models Trained on Code" (https://arxiv.org/abs/2107.03374).

Once you have read this disclaimer and taken appropriate precautions,
set the environment variable HF_ALLOW_CODE_EVAL="1". Within Python you can to this
with:

>>> import os
>>> os.environ["HF_ALLOW_CODE_EVAL"] = "1"

################################################################################\
"""

_LICENSE = """The MIT License

Copyright (c) OpenAI (https://openai.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

def compute_code_eval(predictions, references, k=[1, 10, 100], num_workers=4, timeout=3.0):
    """Returns the scores"""

    if os.getenv("HF_ALLOW_CODE_EVAL", 0) != "1":
        raise ValueError(_WARNING)

    if os.name == "nt":
        raise NotImplementedError("This metric is currently not supported on Windows.")
    task_id_list = [p[0] for p in predictions]
    test_programs = []

    # code pre-process
    new_predictions = []
    assert len(references) == len(predictions)
    for reference, prediction_ in zip(references, predictions):
        candidate = prediction_[1]

        try:
            candidate = eval(candidate)['code']
        except:
            candidate = candidate.replace('{\n  \"code\": \"', '').replace('\"}', '').strip()
            candidate = candidate.replace('{\"code\":\"', '').replace('\"}', '').strip()
            candidate = candidate.replace('{\"code\": \"', '').replace('\"}', '').strip()
            candidate = candidate.replace('{\"code\":  \"', '').replace('\"}', '').strip()
            candidate = candidate.replace('{\"code\":   \"', '').replace('\"}', '').strip()
            candidate = candidate.replace('{\"code\":    \"', '').replace('\"}', '').strip()
        if '# Example usage' in candidate:
            items = candidate.split('# Example usage')
            if len(items) == 2:
                candidate = items[0]
        if '# Test cases' in candidate:
            items = candidate.split('# Test cases')
            if len(items) == 2:
                candidate = items[0]

        if 'assert' in candidate:
            items = [line for line in candidate.split('\n') if 'assert' not in line]
            candidate_ = '\n'.join(items)

        try:
            reference_func_name = find_first_function_name(reference)
            candidate_func_name = find_first_function_name(candidate)
            if reference_func_name != 'check':
                if candidate_func_name != reference_func_name:
                    candidate = candidate.replace(candidate_func_name, reference_func_name)
            else:
                reference_func_name = find_first_function_name(reference.split('\n')[-1])
                if candidate_func_name != reference_func_name:
                    candidate = candidate.replace(candidate_func_name, reference_func_name)
        except:
            pass
        new_predictions.append((prediction_[0], candidate, reference))

    with tqdm(total=len(task_id_list), desc="eval: ") as pbar:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            completion_id = Counter()
            n_samples = 0
            results = defaultdict(list)

            for task_id, candidates, test_case in tqdm(zip(task_id_list, new_predictions, references)):
                assert task_id == candidates[0]

                candidate = candidates[1]
                test_program = candidate + "\n" + test_case
                test_programs.append(test_program)
                args = (test_program, timeout, task_id, completion_id[task_id])
                future = executor.submit(check_correctness, *args)
                futures.append(future)
                completion_id[task_id] += 1
                n_samples += 1
                pbar.update(1)

            for future in as_completed(futures):
                result = future.result()
                results[result["task_id"]].append((result["completion_id"], result))

    total, correct = [], []
    assert len(results) == len(test_programs)
    for index, result in enumerate(results.values()):
        result.sort()
        passed = [r[1]["passed"] for r in result]
        total.append(len(passed))
        correct.append(sum(passed))
        test_program = test_programs[index]
    total = np.array(total)
    correct = np.array(correct)

    ks = k
    if not isinstance(ks, (list, tuple)):
        ks = [ks]
    pass_at_k = {f"pass@{k}": estimate_pass_at_k(total, correct, k).mean() for k in ks if (total >= k).all()}

    return pass_at_k, results


def estimate_pass_at_k(num_samples, num_correct, k):
    """Estimates pass@k of each problem and returns them in an array."""

    def estimator(n: int, c: int, k: int) -> float:
        """Calculates 1 - comb(n - c, k) / comb(n, k)."""
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])
