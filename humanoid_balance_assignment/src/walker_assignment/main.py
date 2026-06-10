from __future__ import annotations

import argparse
import pathlib
import time

import numpy as np

try:
    import mujoco
    import mujoco.viewer
except ImportError as exc:  # pragma: no cover
    raise SystemExit("MuJoCo is not installed. Run: pip install mujoco") from exc

from walker_assignment.controllers import pd_control, lqr_control, lqr_gain
from walker_assignment.plotting import plot_log

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "walker_assignment" / "models" / "simple_inverted_pendulum.xml"


def load_model():
    # Read the XML in Python (handles non-ASCII paths on Windows) and parse
    # from the string, since from_xml_path fails on Unicode paths.
    xml = MODEL_PATH.read_text(encoding="utf-8")
    return mujoco.MjModel.from_xml_string(xml)


def name_of(model, obj_type, idx: int) -> str:
    return mujoco.mj_id2name(model, obj_type, idx) or f"unnamed_{idx}"


def inspect_model() -> None:
    model = load_model()
    print("Model:", MODEL_PATH)
    print("nq =", model.nq, "  nv =", model.nv, "  nu =", model.nu)

    print("\nJoints:")
    for i in range(model.njnt):
        name = name_of(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print(f"  joint[{i}] name={name:10s} qposadr={model.jnt_qposadr[i]} dofadr={model.jnt_dofadr[i]}")

    print("\nActuators:")
    for i in range(model.nu):
        name = name_of(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
        lo, hi = model.actuator_ctrlrange[i]
        print(f"  ctrl[{i}] actuator={name:12s} ctrlrange=[{lo:.1f}, {hi:.1f}] Nm")

    print("\nState meaning:")
    print("  qpos[0] = ankle angle theta [rad], theta=0 is upright")
    print("  qvel[0] = ankle angular velocity theta_dot [rad/s]")
    print("  ctrl[0] = ankle torque [Nm]")
    print("  LQR gain K =", lqr_gain())


def control_signal(mode: str, q: float, qdot: float) -> float:
    if mode == "open_loop":
        return 0.0
    if mode == "pd":
        return pd_control(q, qdot)
    if mode in {"lqr", "perturbation"}:
        return lqr_control(q, qdot)
    raise ValueError(f"Unknown mode: {mode}")


def simulate(mode: str, duration: float, viewer: bool, out_dir: str) -> pathlib.Path:
    model = load_model()
    data = mujoco.MjData(model)

    # Initial condition: small lean from the upright unstable equilibrium.
    data.qpos[0] = 0.15
    data.qvel[0] = 0.0
    mujoco.mj_forward(model, data)

    dt = model.opt.timestep
    n_steps = int(duration / dt)
    log = {
        "t": np.zeros(n_steps),
        "q": np.zeros(n_steps),
        "qdot": np.zeros(n_steps),
        "tau": np.zeros(n_steps),
    }

    def step(k: int):
        q = float(data.qpos[0])
        qdot = float(data.qvel[0])
        tau = control_signal(mode, q, qdot)

        # Disturbance experiment: short kick at t = 2 s.
        if mode == "perturbation" and abs(data.time - 2.0) < 0.5 * dt:
            data.qvel[0] += 2.0

        data.ctrl[0] = tau
        mujoco.mj_step(model, data)

        log["t"][k] = data.time
        log["q"][k] = data.qpos[0]
        log["qdot"][k] = data.qvel[0]
        log["tau"][k] = data.ctrl[0]

    if viewer:
        with mujoco.viewer.launch_passive(model, data) as v:
            for k in range(n_steps):
                step(k)
                v.sync()
                time.sleep(dt)
    else:
        for k in range(n_steps):
            step(k)

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / f"{mode}_log.npz"
    np.savez(log_path, **log)
    plot_log(log_path, out / f"{mode}_plot.png", title=mode)
    print(f"Saved: {log_path}")
    print(f"Saved: {out / (mode + '_plot.png')}")
    return log_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Simplified humanoid balance assignment")
    parser.add_argument("--mode", choices=["inspect", "open_loop", "pd", "lqr", "perturbation"], default="inspect")
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--viewer", action="store_true")
    parser.add_argument("--out-dir", default="results")
    args = parser.parse_args()

    if args.mode == "inspect":
        inspect_model()
    else:
        simulate(args.mode, args.duration, args.viewer, args.out_dir)


if __name__ == "__main__":
    main()
