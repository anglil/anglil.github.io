---
layout: default
title: Angli Liu
---

<div class="wrapper">
  <div class="sidebar">
    <ul>
      <li><a href="https://tech-stuff-angli.quora.com/" target="_blank">Tech Stuff Blog</a></li>
      <li><a href="https://anglil.quora.com/" target="_blank">Personal Blog</a></li>
      <li><a href="https://scholar.google.com/citations?user=lNOZAc4AAAAJ&amp;hl=en" target="_blank">Google Scholar</a></li>
    </ul>
  </div>

  <div class="main">
    <!-- Photo placeholder – floated right, similar placement to many Berkeley/UT faculty pages -->
    <!-- Upload your photo to /images/angli-photo.jpg and uncomment: -->
    <!--
    <img src="/images/angli-photo.jpg" alt="Angli Liu" class="profile-photo">
    -->

    <h1>Angli Liu</h1>

    <div class="title">
      PhD Student<br>
      Paul G. Allen School of Computer Science & Engineering<br>
      University of Washington
    </div>

    <p class="email">
      <a href="mailto:anglil@cs.washington.edu">anglil@cs.washington.edu</a>
    </p>

    <h2>About</h2>
    <p>
      [Add your short bio here – research interests, background, current projects, etc.]
      <br><br>
      I'm a PhD student working on [your main research area]. 
      Previously [brief previous experience/education if you want to include].
    </p>

    <hr>

  </div>
</div>

<style>
  .wrapper {
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px 20px;
    display: flex;
    gap: 60px;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 17px;
    line-height: 1.58;
    color: #222;
  }

  .sidebar {
    width: 220px;
    flex-shrink: 0;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 2em 0 0 0;
  }

  .sidebar li {
    margin: 1.4em 0;
  }

  .sidebar a {
    color: #c4820e;                /* Berkeley-style orange */
    text-decoration: none;
    font-size: 1.1em;
  }

  .sidebar a:hover {
    text-decoration: underline;
    color: #d35400;               /* Darker orange hover */
  }

  .main {
    flex: 1;
  }

  h1 {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-weight: normal;
    font-size: 3em;
    margin: 0 0 0.2em 0;
    color: #000;
  }

  .title {
    font-size: 1.35em;
    color: #444;
    margin-bottom: 1.5em;
  }

  .email {
    font-size: 1.2em;
    margin: 2em 0 3em 0;
  }

  h2 {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-weight: normal;
    font-size: 1.9em;
    margin: 3em 0 0.8em 0;
    color: #000;
  }

  p {
    margin: 1.1em 0;
  }

  a {
    color: #c4820e;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }

  hr {
    border: 0;
    border-top: 1px solid #ddd;
    margin: 3em 0;
  }

  .profile-photo {
    float: right;
    width: 200px;
    height: auto;
    margin: 0 0 2em 2.5em;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
  }

  @media (max-width: 850px) {
    .wrapper {
      flex-direction: column;
      gap: 40px;
    }
    .sidebar {
      width: 100%;
    }
    .profile-photo {
      float: none;
      display: block;
      margin: 0 auto 2em;
    }
  }
</style>