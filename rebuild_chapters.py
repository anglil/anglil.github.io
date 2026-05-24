import os
import glob

# Master script to rebuild all 4 chapters
chapters_data = {
    "ch01": {
        "title": "Circuits Principles, Experiments, and Semiconductors",
        "sections": [
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
"""
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
"""
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
"""
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
"""
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
"""
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
"""
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
"""
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
"""
            }
        ]
    },
    "ch02": {
        "title": "Communication Circuits",
        "sections": [
            {
                "title": "I. Resonant Circuits and Impedance Matching",
                "content": r"""
<p><strong>1. Series and Parallel Resonance</strong></p>
<p>In a series RLC circuit, resonance occurs when the inductive and capacitive reactances cancel out: $\omega_0 L = \frac{1}{\omega_0 C} \implies \omega_0 = \frac{1}{\sqrt{LC}}$. At resonance, the impedance is purely resistive ($Z = R$) and the current is maximized.</p>
<p>The quality factor $Q$ is defined as $Q = \frac{\omega_0 L}{R} = \frac{1}{\omega_0 CR}$. The bandwidth is $BW = \frac{\omega_0}{Q}$.</p>
<p><strong>2. Impedance Matching Networks</strong></p>
<p>Maximum power transfer occurs when the load impedance is the complex conjugate of the source impedance: $Z_L = Z_S^*$. L-sections (LC circuits), Pi-networks, and T-networks are used to transform impedances at radio frequencies without resistive losses.</p>
"""
            },
            {
                "title": "II. High-Frequency and RF Amplifiers",
                "content": r"""
<p><strong>1. Small-Signal High-Frequency Transistor Models</strong></p>
<p>At high frequencies, the parasitic capacitances of BJTs ($C_\pi, C_\mu$) and MOSFETs ($C_{gs}, C_{gd}, C_{ds}$) can no longer be ignored. The unity-gain transition frequency is $f_T = \frac{g_m}{2\pi (C_\pi + C_\mu)}$.</p>
<p><strong>2. The Miller Effect</strong></p>
<p>A capacitance connected between the input and output (like $C_\mu$ or $C_{gd}$) is amplified by the inverting voltage gain of the amplifier, appearing at the input as $C_{in} = C_F (1 - A_v)$. This significantly reduces the high-frequency bandwidth.</p>
<p><strong>3. Tuned Amplifiers</strong></p>
<p>RF amplifiers use tuned LC circuits as loads to provide high gain at a specific center frequency and reject out-of-band signals.</p>
"""
            },
            {
                "title": "III. Oscillators",
                "content": r"""
<p><strong>1. Barkhausen Criterion</strong></p>
<p>For a feedback loop with forward gain $A(s)$ and feedback factor $\beta(s)$, sustained oscillation occurs if:</p>
$$ |A(j\omega_0) \beta(j\omega_0)| = 1 \quad \text{and} \quad \angle(A\beta) = 2\pi n $$
<p><strong>2. LC and Crystal Oscillators</strong></p>
<p>Colpitts and Hartley oscillators use LC tanks to set the oscillation frequency. Quartz crystal oscillators utilize the piezoelectric effect to achieve extremely high $Q$ factors and frequency stability.</p>
"""
            },
            {
                "title": "IV. Amplitude Modulation (AM)",
                "content": r"""
<p><strong>1. AM Fundamentals</strong></p>
<p>In amplitude modulation, the amplitude of a high-frequency carrier wave $A_c \cos(\omega_c t)$ is varied in proportion to the message signal $m(t)$:</p>
$$ s(t) = A_c [1 + k_a m(t)] \cos(\omega_c t) $$
<p>The modulation index is $\mu = k_a \max|m(t)|$. The spectrum contains the carrier and two sidebands.</p>
<p><strong>2. Double Sideband Suppressed Carrier (DSB-SC)</strong></p>
<p>DSB-SC simply multiplies the message and carrier: $s(t) = m(t) \cos(\omega_c t)$. It saves power but requires coherent (synchronous) demodulation.</p>
<p><strong>3. AM Demodulation</strong></p>
<p>Standard AM can be easily demodulated using an envelope detector (a diode followed by an RC low-pass filter). DSB-SC is demodulated using a local oscillator and a low-pass filter.</p>
"""
            },
            {
                "title": "V. Frequency and Phase Modulation (FM/PM)",
                "content": r"""
<p><strong>1. Angle Modulation Concepts</strong></p>
<p>In angle modulation, the phase $\theta(t)$ of the carrier is varied. For Phase Modulation (PM), $\theta(t) = \omega_c t + k_p m(t)$. For Frequency Modulation (FM), the instantaneous frequency $\omega_i(t) = \omega_c + k_f m(t)$, meaning $\theta(t) = \omega_c t + k_f \int m(\tau) d\tau$.</p>
<p><strong>2. FM Bandwidth and Carson's Rule</strong></p>
<p>Unlike AM, FM has an infinite number of sidebands (Bessel functions). However, 98% of the power is contained within a bandwidth approximated by Carson's Rule:</p>
$$ B_T \approx 2 (\Delta f + f_m) $$
<p>where $\Delta f$ is the peak frequency deviation and $f_m$ is the maximum frequency of the message.</p>
<p><strong>3. Phase-Locked Loops (PLL)</strong></p>
<p>A PLL consists of a Phase Detector, a Loop Filter, and a Voltage-Controlled Oscillator (VCO). It tracks the phase of an incoming signal, acting as an excellent FM demodulator and frequency synthesizer.</p>
"""
            }
        ]
    },
    "ch03": {
        "title": "Antennae",
        "sections": [
            {
                "title": "I. Maxwell's Equations and Wave Propagation",
                "content": r"""
<p><strong>1. Maxwell's Equations</strong></p>
<p>Antenna theory is fundamentally grounded in Maxwell's equations. In differential form (time-harmonic fields $e^{j\omega t}$):</p>
$$ \nabla \times \mathbf{E} = -j\omega \mu \mathbf{H} $$
$$ \nabla \times \mathbf{H} = \mathbf{J} + j\omega \varepsilon \mathbf{E} $$
$$ \nabla \cdot \mathbf{D} = \rho_v $$
$$ \nabla \cdot \mathbf{B} = 0 $$
<p><strong>2. The Wave Equation and Retarded Potentials</strong></p>
<p>To find the fields radiated by a current distribution $\mathbf{J}$, we introduce the magnetic vector potential $\mathbf{A}$ and the electric scalar potential $V$. The retarded vector potential is:</p>
$$ \mathbf{A}(\mathbf{r}) = \frac{\mu}{4\pi} \int_V \mathbf{J}(\mathbf{r}') \frac{e^{-jk|\mathbf{r}-\mathbf{r}'|}}{|\mathbf{r}-\mathbf{r}'|} dv' $$
<p>where $k = \omega\sqrt{\mu\varepsilon}$ is the wavenumber.</p>
"""
            },
            {
                "title": "II. Fundamental Parameters of Antennas",
                "content": r"""
<p><strong>1. Radiation Pattern and Solid Angle</strong></p>
<p>The radiation pattern describes the spatial distribution of radiated power as a function of spherical coordinates $(\theta, \phi)$. The beam solid angle $\Omega_A$ is the integral of the normalized power pattern.</p>
<p><strong>2. Directivity, Gain, and Efficiency</strong></p>
<p>Directivity $D$ is the ratio of the radiation intensity in a given direction to the radiation intensity averaged over all directions: $D = \frac{4\pi U(\theta, \phi)}{P_{rad}}$.</p>
<p>Gain $G$ includes the radiation efficiency $e_{rad}$ of the antenna: $G = e_{rad} D$.</p>
<p><strong>3. Input Impedance and Effective Area</strong></p>
<p>The input impedance is $Z_{in} = R_r + R_L + jX_A$, where $R_r$ is the radiation resistance. The effective aperture $A_e$ is related to directivity by: $A_e = \frac{\lambda^2}{4\pi} D$.</p>
"""
            },
            {
                "title": "III. Wire Antennas and Arrays",
                "content": r"""
<p><strong>1. The Hertzian Dipole and Linear Wire Antennas</strong></p>
<p>The infinitesimal (Hertzian) dipole has a radiation resistance of $R_r = 80\pi^2 \left(\frac{l}{\lambda}\right)^2$. A half-wave dipole ($l = \lambda/2$) has a much higher radiation resistance ($R_r \approx 73 \Omega$) and a directivity of 2.15 dBi.</p>
<p><strong>2. Antenna Arrays</strong></p>
<p>To increase directivity, multiple antenna elements are arranged in an array. The total far-field pattern is the product of the element pattern and the Array Factor (AF):</p>
$$ \text{Total Pattern} = \text{Element Pattern} \times AF(\theta, \phi) $$
<p>For a uniform linear array of $N$ elements with spacing $d$ and phase shift $\beta$, $AF = \frac{\sin(N\psi/2)}{\sin(\psi/2)}$, where $\psi = kd\cos\theta + \beta$.</p>
"""
            },
            {
                "title": "IV. Aperture and Microstrip Antennas",
                "content": r"""
<p><strong>1. Aperture Antennas</strong></p>
<p>Horns, waveguides, and parabolic reflectors are examples of aperture antennas. They are analyzed using Huygens' Principle (Equivalence Principle), which states that the fields in an aperture can be replaced by equivalent electric and magnetic surface currents $\mathbf{J}_s$ and $\mathbf{M}_s$.</p>
<p><strong>2. Microstrip (Patch) Antennas</strong></p>
<p>Patch antennas are low-profile, lightweight, and easily integrated with planar circuits. They radiate primarily from the fringing fields between the patch edge and the ground plane. They are often analyzed using the transmission-line model or cavity model.</p>
"""
            }
        ]
    },
    "ch04": {
        "title": "Digital Electronics",
        "sections": [
            {
                "title": "I. Boolean Algebra and Logic Gates",
                "content": r"""
<p><strong>1. Number Systems and Codes</strong></p>
<p>Digital systems operate on binary digits (bits), $0$ and $1$. Common number representations include unsigned binary, two's complement for signed integers, and floating-point for real numbers. Hexadecimal (base-16) is often used as a compact representation.</p>
<p><strong>2. Boolean Algebra</strong></p>
<p>Boolean algebra relies on fundamental operations: AND ($\cdot$), OR ($+$), and NOT ($\overline{x}$). De Morgan's laws state:</p>
$$ \overline{A \cdot B} = \overline{A} + \overline{B} $$
$$ \overline{A + B} = \overline{A} \cdot \overline{B} $$
<p><strong>3. Logic Gates</strong></p>
<p>Basic gates are AND, OR, NOT. Universal gates (NAND, NOR) can be used to construct any logic function. Exclusive-OR (XOR) is widely used in arithmetic circuits.</p>
"""
            },
            {
                "title": "II. Combinational Logic Circuits",
                "content": r"""
<p><strong>1. Minimization Techniques</strong></p>
<p>Boolean functions can be simplified to minimize hardware using algebraic manipulation or Karnaugh Maps (K-maps). The goal is to find the Sum of Products (SOP) or Product of Sums (POS) with the fewest literals.</p>
<p><strong>2. Typical Combinational Components</strong></p>
<ul>
    <li><strong>Adders:</strong> Half-adders and Full-adders. Ripple carry adders are simple but slow due to propagation delay; Carry Lookahead Adders (CLA) are faster.</li>
    <li><strong>Multiplexers (MUX):</strong> Selects one of $2^N$ data inputs based on $N$ select lines.</li>
    <li><strong>Decoders:</strong> Translates an $N$-bit input into up to $2^N$ unique output lines.</li>
</ul>
"""
            },
            {
                "title": "III. Sequential Logic Circuits",
                "content": r"""
<p><strong>1. Latches and Flip-Flops</strong></p>
<p>Unlike combinational logic, sequential logic has memory. An SR Latch is the most basic memory element. A D Flip-Flop updates its output $Q$ to the value of input $D$ precisely at the active edge of a clock signal.</p>
<p><strong>2. Finite State Machines (FSM)</strong></p>
<p>Complex sequential circuits are modeled as FSMs, consisting of a state register, next-state combinational logic, and output combinational logic. In a Moore machine, outputs depend only on the current state. In a Mealy machine, outputs depend on both state and current inputs.</p>
<p><strong>3. Registers and Counters</strong></p>
<p>Shift registers are used for data storage and serial/parallel conversion. Counters iterate through a defined sequence of states (e.g., binary up counter).</p>
"""
            }
        ]
    }
}

img_dir = "college-electrical-engineering/images"

def generate_chapter(ch_id, ch_num):
    data = chapters_data[ch_id]
    
    # Get all diagrams for this chapter
    diagrams = sorted(glob.glob(os.path.join(img_dir, f"crop_{ch_id}_*.png")))
    
    # Distribute diagrams evenly across sections
    num_sections = len(data["sections"])
    diags_per_section = len(diagrams) // num_sections
    remainder = len(diagrams) % num_sections
    
    html_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter {ch_num}: {data['title']} | College Electrical Engineering</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script>
      window.MathJax = {{
          tex: {{
              inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],
              displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],
              macros: {{
                  bm: ["\\\\boldsymbol{{#1}}", 1]
              }}
          }}
      }};
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
      <li><a href="ch01.html"{' class="active"' if ch_num == 1 else ''}>Chapter 1: Circuits & Semiconductors</a></li>
      <li><a href="ch02.html"{' class="active"' if ch_num == 2 else ''}>Chapter 2: Communication Circuits</a></li>
      <li><a href="ch03.html"{' class="active"' if ch_num == 3 else ''}>Chapter 3: Antennae</a></li>
      <li><a href="ch04.html"{' class="active"' if ch_num == 4 else ''}>Chapter 4: Digital Electronics</a></li>
    </ul>
  </nav>
</aside>

<main id="content">
  <div class="chapter-header">
    <h1>Chapter {ch_num}</h1>
    <h2 class="chapter-title">{data['title']}</h2>
  </div>
"""

    html_tail = """
</main>
</body>
</html>
"""

    body = ""
    diag_idx = 0
    
    for i, sec in enumerate(data["sections"]):
        body += f"\n  <h3>{sec['title']}</h3>\n"
        body += sec['content']
        body += '\n  <div class="pages-container">\n'
        
        count = diags_per_section + (1 if i < remainder else 0)
        for _ in range(count):
            if diag_idx < len(diagrams):
                img_name = os.path.basename(diagrams[diag_idx])
                body += f'    <img src="images/{img_name}" class="page-img diagram-img" style="max-width:80%; height:auto; display:block; margin: 20px auto; border: 1px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" alt="Extracted Diagram">\n'
                diag_idx += 1
        body += '  </div>\n'

    full_html = html_head + body + html_tail

    with open(f"college-electrical-engineering/{ch_id}.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Chapter {ch_num} ({ch_id}) rebuilt with {len(diagrams)} extracted diagrams.")

generate_chapter("ch01", 1)
generate_chapter("ch02", 2)
generate_chapter("ch03", 3)
generate_chapter("ch04", 4)

