#*********************************************************** Experiment configuration shared by all Smart HPA components ***********************************************************
#
# The original package hard-codes the scenario (5R-50%) in all 11 Microservice Managers and the test time in the
# Microservice Capacity Analyzer. Here they are read from environment variables so one run script can switch scenarios.
#
#   SMARTHPA_SCENARIO   e.g. "5R-50%" (default) or "2R-20%"  -> "<maxR>R-<CPU threshold>%"
#   SMARTHPA_DURATION   total test time in seconds (default 900 = 15 minutes, as in the paper)
#   SMARTHPA_ARM        "paper" (default) = Adaptive_Resource_Manager.py, the authors' Algorithm 2
#                       "priority"        = Priority_Resource_Manager.py, improvement C3
#                       "flat"            = Priority_Resource_Manager.py with every weight 1 and no headroom: control
#                                           run of C3, keeps only its fix of the lost quota (W9)

import os
import re

SCENARIO = os.environ.get("SMARTHPA_SCENARIO", "5R-50%")

_match = re.fullmatch(r"(\d+)R-(\d+)%?", SCENARIO)
if _match is None:
    raise ValueError(f"SMARTHPA_SCENARIO must look like '5R-50%', got {SCENARIO!r}")

MAX_REPLICA = int(_match.group(1))
TARGET_CPU = int(_match.group(2))
MIN_REPLICA = 1

TEST_DURATION = int(os.environ.get("SMARTHPA_DURATION", "900"))

ARM_VARIANT = os.environ.get("SMARTHPA_ARM", "paper")
if ARM_VARIANT not in ("paper", "priority", "flat"):
    raise ValueError(f"SMARTHPA_ARM must be 'paper', 'priority' or 'flat', got {ARM_VARIANT!r}")


#*********************************************************** Retry transient kubectl failures ***********************************************************
#
# The Microservice Managers call kubectl through subprocess.check_output with no error handling, so ONE failed call
# (e.g. the API server briefly not answering while 11 processes poll it) kills the whole run. This happened in
# 5R-50% Smart HPA run 3 (02/10). Every manager imports this module, so patching check_output here adds retries without
# touching the scaling algorithm. Used by both Smart HPA and the K8s HPA observer, so both are measured the same way.

import subprocess
import sys
import time

_original_check_output = subprocess.check_output
KUBECTL_RETRIES = 5
KUBECTL_RETRY_DELAY_SEC = 2


def _check_output_with_retry(cmd, *args, **kwargs):
    for attempt in range(1, KUBECTL_RETRIES + 1):
        try:
            return _original_check_output(cmd, *args, **kwargs)
        except subprocess.CalledProcessError as exc:
            if attempt == KUBECTL_RETRIES:
                raise
            print(f"[retry] {time.strftime('%H:%M:%S')} attempt {attempt} failed (exit {exc.returncode}): {' '.join(map(str, cmd))}",
                  file=sys.stderr, flush=True)
            time.sleep(KUBECTL_RETRY_DELAY_SEC)


subprocess.check_output = _check_output_with_retry
