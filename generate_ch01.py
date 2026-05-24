import math

sections = [
    {
        "title": "I. Circuit Variables and Basic Laws",
        "content": r"""
<p><strong>1. Charge and Current</strong></p>
<p>Electric charge $q$ is the fundamental property of matter. The unit of charge is the Coulomb (C). Electric current $i$ is the time rate of change of charge, measured in Amperes (A):</p>
$$ i = \frac{dq}{dt} $$
<p><strong>2. Voltage, Power, and Energy</strong></p>
<p>Voltage $v$ (or potential difference) is the energy required to move a unit charge through an element, measured in Volts (V): $v = \frac{dw}{dq}$. Power $p$ is the time rate of expending or absorbing energy, measured in Watts (W):</p>
$$ p = \frac{dw}{dt} = \left(\frac{dw}{dq}\right)\left(\frac{dq}{dt}\right) = v i $$
<p><strong>3. Ohm's Law and Ideal Sources</strong></p>
<p>Ohm's Law states that the voltage across a resistor is directly proportional to the current flowing through it: $v = i R$. The resistance $R$ is measured in Ohms ($\Omega$). The conductance $G = \frac{1}{R}$ is measured in Siemens (S).</p>
<p>Ideal voltage and current sources maintain a prescribed voltage or current regardless of the rest of the circuit.</p>
<p><strong>4. Kirchhoff's Laws</strong></p>
<ul>
    <li><strong>Kirchhoff's Current Law (KCL):</strong> The algebraic sum of currents entering a node is zero: $\sum_{n=1}^N i_n = 0$.</li>
    <li><strong>Kirchhoff's Voltage Law (KVL):</strong> The algebraic sum of all voltages around a closed path (or loop) is zero: $\sum_{m=1}^M v_m = 0$.</li>
</ul>
""",
        "img_start": 1,
        "img_end": 12
    },
    {
        "title": "II. Resistive Circuits and Analysis Methods",
        "content": r"""
<p><strong>1. Series and Parallel Resistors</strong></p>
<p>For $N$ resistors in series, the equivalent resistance is $R_{eq} = \sum_{i=1}^N R_i$. For parallel resistors, the equivalent conductance is $G_{eq} = \sum_{i=1}^N G_i$, or $\frac{1}{R_{eq}} = \sum_{i=1}^N \frac{1}{R_i}$.</p>
<p><strong>2. Voltage and Current Division</strong></p>
<p>Voltage division for two resistors in series: $v_1 = \frac{R_1}{R_1 + R_2} v_s$. Current division for two resistors in parallel: $i_1 = \frac{R_2}{R_1 + R_2} i_s$.</p>
<p><strong>3. Nodal and Mesh Analysis</strong></p>
<p>Nodal analysis involves applying KCL to non-reference nodes to determine node voltages. Mesh analysis involves applying KVL to independent loops to determine mesh currents.</p>
<p><strong>4. Superposition and Source Transformation</strong></p>
<p>The superposition principle states that the response in a linear circuit with multiple independent sources is the sum of the responses caused by each independent source acting alone.</p>
<p><strong>5. Thevenin's and Norton's Theorems</strong></p>
<p>Thevenin's Theorem states that any linear two-terminal circuit can be replaced by an equivalent circuit consisting of a voltage source $V_{Th}$ in series with a resistor $R_{Th}$. Norton's Theorem replaces it with a current source $I_N$ in parallel with $R_N$.</p>
$$ V_{Th} = V_{oc} \quad I_N = I_{sc} \quad R_{Th} = R_N = \frac{V_{oc}}{I_{sc}} $$
""",
        "img_start": 13,
        "img_end": 25
    },
    {
        "title": "III. Operational Amplifiers",
        "content": r"""
<p><strong>1. The Ideal Op-Amp</strong></p>
<p>An operational amplifier is a voltage-controlled voltage source. The ideal op-amp model assumes:</p>
<ol>
    <li>Infinite input impedance: $R_{in} = \infty \implies i_+ = i_- = 0$</li>
    <li>Zero output impedance: $R_{out} = 0$</li>
    <li>Infinite open-loop gain: $A = \infty \implies v_+ = v_-$ (virtual short)</li>
</ol>
<p><strong>2. Inverting and Non-inverting Amplifiers</strong></p>
<p>For an inverting amplifier with input resistor $R_1$ and feedback resistor $R_f$: $v_{out} = -\frac{R_f}{R_1} v_{in}$.</p>
<p>For a non-inverting amplifier: $v_{out} = \left(1 + \frac{R_f}{R_1}\right) v_{in}$.</p>
<p><strong>3. Summing and Difference Amplifiers</strong></p>
<p>Op-amps can be configured to perform mathematical operations such as addition, subtraction, integration, and differentiation.</p>
""",
        "img_start": 26,
        "img_end": 38
    },
    {
        "title": "IV. Energy Storage Elements and Transients",
        "content": r"""
<p><strong>1. Capacitors and Inductors</strong></p>
<p>A capacitor stores energy in its electric field. The current-voltage relationship is $i = C \frac{dv}{dt}$. Energy stored: $W = \frac{1}{2} C v^2$.</p>
<p>An inductor stores energy in its magnetic field. The voltage-current relationship is $v = L \frac{di}{dt}$. Energy stored: $W = \frac{1}{2} L i^2$.</p>
<p><strong>2. First-Order Circuits (RC and RL)</strong></p>
<p>The response of a first-order circuit can be decomposed into a natural response and a forced response, or transient and steady-state components.</p>
$$ x(t) = x(\infty) + [x(0) - x(\infty)] e^{-t/\tau} $$
<p>For an RC circuit, the time constant is $\tau = RC$. For an RL circuit, $\tau = \frac{L}{R}$.</p>
<p><strong>3. Second-Order Circuits (RLC)</strong></p>
<p>The step response of a series RLC circuit is described by a second-order differential equation. The behavior depends on the damping ratio $\zeta$ and the undamped natural frequency $\omega_n$. It can be overdamped, critically damped, or underdamped.</p>
""",
        "img_start": 39,
        "img_end": 50
    },
    {
        "title": "V. AC Steady-State Analysis",
        "content": r"""
<p><strong>1. Sinusoids and Phasors</strong></p>
<p>A sinusoidal voltage $v(t) = V_m \cos(\omega t + \phi)$ can be represented by a phasor $\mathbf{V} = V_m e^{j\phi} = V_m \angle \phi$. Phasors transform differential equations into algebraic equations.</p>
<p><strong>2. Impedance and Admittance</strong></p>
<p>The impedance $\mathbf{Z}$ is the ratio of the phasor voltage to the phasor current: $\mathbf{Z} = \frac{\mathbf{V}}{\mathbf{I}} = R + jX$.</p>
<ul>
    <li>Resistor: $\mathbf{Z}_R = R$</li>
    <li>Inductor: $\mathbf{Z}_L = j\omega L$</li>
    <li>Capacitor: $\mathbf{Z}_C = \frac{1}{j\omega C}$</li>
</ul>
<p><strong>3. AC Power Analysis</strong></p>
<p>The average (real) power is $P = V_{rms} I_{rms} \cos(\theta_v - \theta_i)$. The apparent power is $S = V_{rms} I_{rms}$. The complex power is $\mathbf{S} = \mathbf{V}_{rms} \mathbf{I}_{rms}^* = P + jQ$, where $Q$ is the reactive power.</p>
""",
        "img_start": 51,
        "img_end": 65
    },
    {
        "title": "VI. Semiconductor Physics Fundamentals",
        "content": r"""
<p><strong>1. Intrinsic and Extrinsic Semiconductors</strong></p>
<p>Silicon is the most common semiconductor. At absolute zero, it acts as an insulator. Thermal energy generates electron-hole pairs: $n_i^2 = n p$.</p>
<p>Doping introduces impurities to increase conductivity. N-type semiconductors are doped with pentavalent donor atoms ($N_D \gg n_i$), making electrons the majority carriers: $n \approx N_D$. P-type semiconductors are doped with trivalent acceptor atoms ($N_A \gg n_i$), making holes the majority carriers: $p \approx N_A$.</p>
<p><strong>2. Drift and Diffusion Currents</strong></p>
<p>Total current in a semiconductor consists of drift (driven by electric field $E$) and diffusion (driven by concentration gradients):</p>
$$ J_n = q \mu_n n E + q D_n \frac{dn}{dx} $$
$$ J_p = q \mu_p p E - q D_p \frac{dp}{dx} $$
<p>Einstein relation connects mobility and diffusion coefficient: $\frac{D_n}{\mu_n} = \frac{D_p}{\mu_p} = V_T = \frac{kT}{q}$.</p>
""",
        "img_start": 66,
        "img_end": 75
    },
    {
        "title": "VII. PN Junctions and Diodes",
        "content": r"""
<p><strong>1. The PN Junction in Equilibrium</strong></p>
<p>When P and N regions are joined, a depletion region forms due to carrier diffusion. A built-in potential barrier $V_0$ prevents further diffusion:</p>
$$ V_0 = V_T \ln\left(\frac{N_A N_D}{n_i^2}\right) $$
<p><strong>2. Forward and Reverse Bias</strong></p>
<p>Under forward bias ($V_D > 0$), the barrier is lowered, allowing significant diffusion current. Under reverse bias ($V_D < 0$), the barrier is widened, resulting in a tiny reverse saturation current $I_S$.</p>
<p>The ideal diode equation (Shockley equation) is:</p>
$$ I_D = I_S \left( e^{\frac{V_D}{n V_T}} - 1 \right) $$
<p><strong>3. Diode Applications</strong></p>
<p>Diodes are used in half-wave and full-wave rectifiers, voltage regulators (using Zener diodes), clippers, and clampers.</p>
""",
        "img_start": 76,
        "img_end": 85
    },
    {
        "title": "VIII. Transistors: BJTs and MOSFETs",
        "content": r"""
<p><strong>1. Bipolar Junction Transistors (BJT)</strong></p>
<p>A BJT has three terminals: Emitter, Base, and Collector. It can be NPN or PNP. In the active region (Emitter-Base junction forward-biased, Collector-Base junction reverse-biased), the collector current is controlled by the base current: $I_C = \beta I_B$.</p>
<p>Small-signal parameters include transconductance $g_m = \frac{I_C}{V_T}$ and input resistance $r_\pi = \frac{\beta}{g_m}$.</p>
<p><strong>2. Metal-Oxide-Semiconductor Field-Effect Transistors (MOSFET)</strong></p>
<p>A MOSFET has four terminals: Gate, Drain, Source, and Body. The drain current $I_D$ is controlled by the gate-to-source voltage $V_{GS}$.</p>
<p>In the saturation region ($V_{GS} > V_{tn}$ and $V_{DS} \ge V_{GS} - V_{tn}$):</p>
$$ I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{tn})^2 (1 + \lambda V_{DS}) $$
<p><strong>3. Transistor Biasing and Amplifiers</strong></p>
<p>DC biasing establishes the quiescent operating point (Q-point). Small-signal AC models are used to analyze voltage gain, input impedance, and output impedance of amplifier configurations (Common Emitter/Source, Common Collector/Drain, Common Base/Gate).</p>
""",
        "img_start": 86,
        "img_end": 95
    }
]

html_head = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 1: Circuits Principles, Experiments, and Semiconductors | College Electrical Engineering</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script>
      window.MathJax = {
          tex: {
              inlineMath: [["$", "$"], ["\\(", "\\)"]],
              displayMath: [["$$", "$$"], ["\\[", "\\]"]],
              macros: {
                  bm: ["\\boldsymbol{#1}", 1]
              }
          }
      };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

<button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>

<aside id="sidebar">
  <div class="book-title">College Electrical Eng<span>Angli Liu</span></div>
  <nav>
    <ul>
      <li><a href="index.html">Table of Contents</a></li>
      <li><div class="part-label">Contents</div></li>
      <li><a href="ch01.html" class="active">Chapter 1: Circuits & Semiconductors</a></li>
      <li><a href="ch02.html">Chapter 2: Communication Circuits</a></li>
      <li><a href="ch03.html">Chapter 3: Antennae</a></li>
      <li><a href="ch04.html">Chapter 4: Digital Electronics</a></li>
    </ul>
  </nav>
</aside>

<main id="content">
  <div class="chapter-header">
    <h1>Chapter 1</h1>
    <h2 class="chapter-title">Circuits Principles, Experiments, and Semiconductors</h2>
  </div>
"""

html_tail = r"""
</main>
</body>
</html>
"""

body = ""
for sec in sections:
    body += f"\n  <h3>{sec['title']}</h3>\n"
    body += sec['content']
    body += '\n  <div class="pages-container">\n'
    for img_num in range(sec['img_start'], sec['img_end'] + 1):
        body += f'    <img src="images/ch01_page_{img_num:03d}.png" class="page-img" alt="Page {img_num}">\n'
    body += '  </div>\n'

full_html = html_head + body + html_tail

with open("college-electrical-engineering/ch01.html", "w", encoding="utf-8") as f:
    f.write(full_html)
