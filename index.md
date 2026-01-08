---
layout: default
title: Home
---

<div class="container">
  <div style="text-align: center; margin: 2em 0;">
    {% if site.avatar %}
    <img src="{{ site.avatar }}" alt="Angli Liu" style="border-radius: 50%; width: 180px; height: 180px; object-fit: cover;">
    {% endif %}
    <h1 style="margin: 0.5em 0;">Angli Liu</h1>
    <h3>PhD Student, Paul G. Allen School of Computer Science & Engineering<br>University of Washington</h3>
  </div>

  <h2>Bio</h2>
  <p>Short bio paragraph here. Add your research interests, background, etc. (replace this text).</p>

  <h2>Contact</h2>
  <p>Email: <a href="mailto:anglil@cs.washington.edu">anglil@cs.washington.edu</a></p>

  <h2>Work / Downloads</h2>
  <ul>
    <li><a href="fg791pip.txt">Download 1</a></li>
    <li><a href="fg791pxe.txt">Download 2</a></li>
  </ul>

  <!-- NEW SECTION 1: Tech Stuff Blog -->
  <h2>Tech Stuff Blog</h2>
  <div class="blog-section">
    <iframe src="https://tech-stuff-angli.quora.com/" width="100%" height="1000px" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></iframe>
  </div>

  <!-- NEW SECTION 2: Personal Blog -->
  <h2>Personal Blog</h2>
  <div class="blog-section">
    <iframe src="https://anglil.quora.com/" width="100%" height="1000px" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></iframe>
  </div>

</div>

<style>
/* Academic-style clean layout */
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

h1, h2, h3 {
  color: #2c3e50;
  margin-top: 2.5em;
  margin-bottom: 1em;
}

h1 { font-size: 2.5em; font-weight: 300; }
h2 { font-size: 1.8em; font-weight: 400; border-bottom: 2px solid #ecf0f1; padding-bottom: 0.5em; }
h3 { font-size: 1.4em; font-weight: 400; }

.blog-section {
  margin: 2em 0;
  background: #fafbfc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

iframe {
  display: block;
  min-height: 1000px;
}

/* Responsive design */
@media (max-width: 768px) {
  .container { padding: 0 15px; }
  iframe { min-height: 800px; }
}
</style>