import math

from checkmate.core.dfgraph import DFGraph
from checkmate.core.schedule import ScheduledResult
from checkmate.core.utils.solver_common import gen_s_matrix_fixed_checkpoints, solve_r_opt
from checkmate.core.enum_strategy import SolveStrategy
from checkmate.core.utils.scheduler import schedule_from_rs
from checkmate.core.utils.timer import Timer


def solve_chen_greedy(g: DFGraph, segment_mem_B: int, use_actuation_points: bool = True):
    with Timer("solve_chen_greedy") as timer_solve:
        C = g.articulation_points if use_actuation_points else g.v
        temp = 0
        x = 0
        checkpoints = set()
        for v in g.topological_order_fwd:
            temp += g.cost_ram[v]
            if v in C and temp > segment_mem_B:
                x += g.cost_ram[v]
                temp = 0
                checkpoints.add(v)
        S = gen_s_matrix_fixed_checkpoints(g, checkpoints)
        R = solve_r_opt(g, S)
    schedule, aux_data = schedule_from_rs(g, R, S)
    return ScheduledResult(
        solve_strategy=SolveStrategy.CHEN_GREEDY if use_actuation_points else SolveStrategy.CHEN_GREEDY_NOAP,
        solver_budget=segment_mem_B,
        feasible=True,
        schedule=schedule,
        schedule_aux_data=aux_data,
        solve_time_s=timer_solve.elapsed,
    )


def solve_chen_sqrtn(g: DFGraph, use_actuation_points: bool = True) -> ScheduledResult:
    with Timer("solve_chen_sqrtn") as timer_solve:
        C = g.articulation_points if use_actuation_points else g.v
        k = int(math.sqrt(len(C)))
        checkpoints = [v for idx, v in enumerate(C) if (idx + 1) % k == 0]
        S = gen_s_matrix_fixed_checkpoints(g, set(checkpoints))
        R = solve_r_opt(g, S)
    schedule, aux_data = schedule_from_rs(g, R, S)
    return ScheduledResult(
        solve_strategy=SolveStrategy.CHEN_SQRTN if use_actuation_points else SolveStrategy.CHEN_SQRTN_NOAP,
        solver_budget=0,
        feasible=True,
        schedule=schedule,
        schedule_aux_data=aux_data,
        solve_time_s=timer_solve.elapsed,
    )
