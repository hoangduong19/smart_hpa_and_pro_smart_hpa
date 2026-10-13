
# Improvement C3 (plan.md section 7): Adaptive Resource Manager that exchanges quota by microservice priority.
# Drop-in replacement for Adaptive_Resource_Manager (same input, same output), selected with SMARTHPA_ARM=priority.
#
# Differences from the paper's Algorithm 2 (Adaptive_Resource_Manager.py, left untouched):
#   1. Underprovisioned microservices are served in descending order of weight x required CPU (paper: required CPU only).
#   2. An overprovisioned microservice with weight >= 2 keeps HEADROOM spare replica(s) out of the exchange, so its
#      capacity is never cut down to exactly its current demand.
#   3. Quota that is left after serving the underprovisioned goes back to the highest weight first, i.e. quota is
#      taken from the lowest weights first (paper: least overprovisioned first).
#   4. The exchange starts from the application's total quota (SLA maxR x CPU request, summed over all microservices)
#      instead of only this iteration's residuals, so quota that could not be handed back in one iteration (a rest
#      smaller than one replica) is offered again in the next one. The original code loses it for the rest of the run.

import math
import config


# Role in the user-facing request path of Online Boutique: every page goes through frontend; it calls productcatalog
# and currency on every page, cart and checkout on the purchase path. Microservices not listed have weight 1.
WEIGHTS = {"frontend": 3, "checkoutservice": 2, "cartservice": 2, "productcatalogservice": 2, "currencyservice": 2}
HEADROOM = 1                    # spare replicas kept by an overprovisioned microservice of weight >= 2


def Priority_Resource_Manager(microservices_data):

    # microservice_data = [microservice_name, SD, DR, CR, CPU request, maxR]; maxR is the capacity left by the previous ARM decision

    SLA_maxR = config.MAX_REPLICA
    Total_Residual_CPU = sum(SLA_maxR * ms[4] for ms in microservices_data)        # the application's whole quota, handed out below


    # ******************************************************************** Microservice Resource Inspector *************************************************************************************

    Underprovisoned_MS = []                         # [microservice_name, required replicas, CPU request, CR, maxR, weight]
    Overprovisioned_MS = []                         # [microservice_name, SD, DR, CPU request, kept replicas, replicas it may get back, weight]

    for name, scaling_action, Desired_Replicas, Current_Replicas, CPU_request, maxR in microservices_data:
        weight = WEIGHTS.get(name, 1)

        if Desired_Replicas > maxR:
            Underprovisoned_MS.append([name, Desired_Replicas - maxR, CPU_request, Current_Replicas, maxR, weight])
            Total_Residual_CPU -= maxR * CPU_request

        else:
            Residual_Replicas = maxR - max(Desired_Replicas, config.MIN_REPLICA)
            Reserved_Replicas = min(HEADROOM, Residual_Replicas) if weight >= 2 else 0
            Kept_Replicas = maxR - Residual_Replicas + Reserved_Replicas
            Returnable_Replicas = max(maxR, SLA_maxR) - Kept_Replicas                  # up to what it holds now, or its SLA maxR if it gave quota away earlier
            Overprovisioned_MS.append([name, scaling_action, Desired_Replicas, CPU_request, Kept_Replicas, Returnable_Replicas, weight])
            Total_Residual_CPU -= Kept_Replicas * CPU_request


    # ******************************************************************** Microservice Resource Balancer *************************************************************************************

    ARM_decision = []                                            # ARM current scaling decision details

    Underprovisoned_MS = sorted(Underprovisoned_MS, key=lambda x: x[5] * x[1] * x[2], reverse=True)       # weight x required CPU, most important shortage first

    for name, Required_Replicas, CPU_request, Current_Replicas, maxR, weight in Underprovisoned_MS:
        Granted_Replicas = min(Required_Replicas, math.floor(Total_Residual_CPU / CPU_request))

        if Granted_Replicas >= 1:
            scaling_action = "scale up"
            Feasible_Replicas = ARM_maxR = maxR + Granted_Replicas
            Total_Residual_CPU -= Granted_Replicas * CPU_request

        else:                                                    # nothing to give: the microservice may still grow up to the capacity it already has
            ARM_maxR = maxR
            scaling_action = "scale up" if Current_Replicas < maxR else "no scale"
            Feasible_Replicas = maxR if Current_Replicas < maxR else Current_Replicas

        ARM_decision.append([name, scaling_action, Feasible_Replicas, ARM_maxR, CPU_request])


    # The remaining quota goes back to the overprovisioned microservices, highest weight first (least overprovisioned first within a weight)

    Overprovisioned_MS = sorted(Overprovisioned_MS, key=lambda x: (-x[6], x[5] * x[3]))

    for name, scaling_action, Desired_Replicas, CPU_request, Kept_Replicas, Returnable_Replicas, weight in Overprovisioned_MS:
        Returned_Replicas = min(Returnable_Replicas, math.floor(Total_Residual_CPU / CPU_request))
        ARM_maxR = Kept_Replicas + Returned_Replicas
        Total_Residual_CPU -= Returned_Replicas * CPU_request

        ARM_decision.append([name, scaling_action, Desired_Replicas, ARM_maxR, CPU_request])

    return ARM_decision           #  same format as Adaptive_Resource_Manager: [microservice_name, scaling action, replicas to set, new maxR, CPU request]
