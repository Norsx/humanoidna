from __future__ import annotations

import pathlib
import numpy as np
import matplotlib.pyplot as plt


def plot_log(log_path: str | pathlib.Path, out_path: str | pathlib.Path, title: str = "") -> None:
    data = np.load(log_path)
    t = data["t"]

    fig1 = plt.figure(figsize=(8, 4))
    plt.plot(t, data["q"], label="theta [rad]")
    plt.plot(t, data["qdot"], label="theta_dot [rad/s]")
    plt.xlabel("time [s]")
    plt.grid(True)
    plt.legend()
    plt.title(f"State response: {title}")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close(fig1)

    torque_path = pathlib.Path(out_path).with_name(pathlib.Path(out_path).stem + "_torque.png")
    fig2 = plt.figure(figsize=(8, 3))
    plt.plot(t, data["tau"], label="tau [Nm]")
    plt.xlabel("time [s]")
    plt.grid(True)
    plt.legend()
    plt.title(f"Control signal: {title}")
    plt.tight_layout()
    plt.savefig(torque_path)
    plt.close(fig2)
