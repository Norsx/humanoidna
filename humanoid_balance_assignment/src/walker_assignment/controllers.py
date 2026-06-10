import numpy as np
from scipy.linalg import solve_continuous_are


def clamp_tau(tau: float, tau_max: float = 30.0) -> float:
    """Saturate ankle torque to actuator limits."""
    return float(np.clip(tau, -tau_max, tau_max))


def pd_control(q: float, qdot: float, q_ref: float = 0.0, qdot_ref: float = 0.0) -> float:
    """PD ankle torque controller.

    Student task:
    - tune Kp and Kd
    - compare weak, acceptable and aggressive gains
    """
    # TODO 1: tune these gains.
    Kp = 1.0
    Kd = 1.0

    tau = Kp * (q_ref - q) + Kd * (qdot_ref - qdot)
    return clamp_tau(tau)


def lqr_matrices(g: float = 9.81, length: float = 0.45, mass: float = 6.0):
    """Linearized inverted-pendulum model around upright position.

    State: x = [theta, theta_dot]^T
    Input: u = ankle torque [Nm]

    theta_ddot = g / length * theta + 1 / (mass * length**2) * u
    """
    A = np.array([[0.0, 1.0],
                  [g / length, 0.0]])
    B = np.array([[0.0],
                  [1.0 / (mass * length**2)]])
    return A, B


def lqr_gain():
    """Return continuous-time LQR gain K.

    Student task:
    - choose Q and R
    - solve the Riccati equation
    - return K = R^{-1} B^T P
    """
    A, B = lqr_matrices()

    # TODO 2: change Q and R and explain their effect.
    Q = np.diag([80.0, 8.0])
    R = np.array([[1.0]])

    # TODO 3: this is already implemented as a starter.
    # Students may keep it, but must explain what it computes.
    P = solve_continuous_are(A, B, Q, R)
    K = np.linalg.solve(R, B.T @ P)
    return K


def lqr_control(q: float, qdot: float) -> float:
    """LQR ankle torque controller."""
    K = lqr_gain()
    x = np.array([[q], [qdot]])
    tau = -float(K @ x)
    return clamp_tau(tau)
