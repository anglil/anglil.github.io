import math

sections = [
    {
        "title": "I. Resonant Circuits and Impedance Matching",
        "content": r"""
<p><strong>1. Series and Parallel Resonance</strong></p>
<p>In a series RLC circuit, resonance occurs when the inductive and capacitive reactances cancel out: $\omega_0 L = \frac{1}{\omega_0 C} \implies \omega_0 = \frac{1}{\sqrt{LC}}$. At resonance, the impedance is purely resistive ($Z = R$) and the current is maximized.</p>
<p>The quality factor $Q$ is defined as $Q = \frac{\omega_0 L}{R} = \frac{1}{\omega_0 CR}$. The bandwidth is $BW = \frac{\omega_0}{Q}$.</p>
<p><strong>2. Impedance Matching Networks</strong></p>
<p>Maximum power transfer occurs when the load impedance is the complex conjugate of the source impedance: $Z_L = Z_S^*$. L-sections (LC circuits), Pi-networks, and T-networks are used to transform impedances at radio frequencies without resistive losses.</p>
""",
        "img_start": 1,
        "img_end": 10
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
""",
        "img_start": 11,
        "img_end": 20
    },
    {
        "title": "III. Oscillators",
        "content": r"""
<p><strong>1. Barkhausen Criterion</strong></p>
<p>For a feedback loop with forward gain $A(s)$ and feedback factor $\beta(s)$, sustained oscillation occurs if:</p>
$$ |A(j\omega_0) \beta(j\omega_0)| = 1 \quad \text{and} \quad \angle(A\beta) = 2\pi n $$
<p><strong>2. LC and Crystal Oscillators</strong></p>
<p>Colpitts and Hartley oscillators use LC tanks to set the oscillation frequency. Quartz crystal oscillators utilize the piezoelectric effect to achieve extremely high $Q$ factors and frequency stability.</p>
""",
        "img_start": 21,
        "img_end": 30
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
""",
        "img_start": 31,
        "img_end": 42
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
""",
        "img_start": 43,
        "img_end": 55
    }
]

html_head = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 2: Communication Circuits | College Electrical Engineering</title>
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
      <li><a href="ch01.html">Chapter 1: Circuits & Semiconductors</a></li>
      <li><a href="ch02.html" class="active">Chapter 2: Communication Circuits</a></li>
      <li><a href="ch03.html">Chapter 3: Antennae</a></li>
      <li><a href="ch04.html">Chapter 4: Digital Electronics</a></li>
    </ul>
  </nav>
</aside>

<main id="content">
  <div class="chapter-header">
    <h1>Chapter 2</h1>
    <h2 class="chapter-title">Communication Circuits</h2>
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
        body += f'    <img src="images/ch02_page_{img_num:03d}.png" class="page-img" alt="Page {img_num}">\n'
    body += '  </div>\n'

full_html = html_head + body + html_tail

with open("college-electrical-engineering/ch02.html", "w", encoding="utf-8") as f:
    f.write(full_html)
print("Chapter 2 generated.")
