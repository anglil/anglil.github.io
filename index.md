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
      <li><a href="#">Notes</a></li>
      <li><a href="https://github.com/anglil" target="_blank">GitHub</a></li>
    </ul>
  </div>

  <div class="main">
    <!-- Photo placeholder – floated right -->
    <!-- Upload your photo to /images/angli-photo.jpg and uncomment: -->
    <!--
    <img src="/images/angli-photo.jpg" alt="Angli Liu" class="profile-photo">
    -->

    <h1>Angli Liu</h1>

    <p>Mind and hand</p>

    <p>
      <a href="mailto:anglil@cs.washington.edu">anglil@cs.washington.edu</a>
    </p>

    <p>San Mateo, California</p>

    <hr>

  </div>
</div>

<style>
  .wrapper {
    max-width: 960px;
    margin: 0 auto;
    padding: 35px 25px 50px;
    display: flex;
    gap: 50px;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 14px;
    line-height: 1.50;
    color: #222;
  }

  .sidebar {
    width: 200px;
    flex-shrink: 0;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 1.8em 0 0 0;
  }

  .sidebar li {
    margin: 1.1em 0;
  }

  .sidebar a {
    color: #c4820e;
    text-decoration: none;
    font-size: 13.5px;
  }

  .sidebar a:hover {
    text-decoration: underline;
    color: #d35400;
  }

  .main {
    flex: 1;
  }

  h1 {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-weight: normal;
    font-size: 2.35em;
    margin: 0 0 0.15em 0;
    color: #000;
  }

  p {
    font-family: Georgia, "Times New Roman", Times, serif;
    margin: 0.95em 0;
    color: #444;
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
    margin: 2.5em 0;
  }

  .profile-photo {
    float: right;
    width: 180px;
    height: auto;
    margin: 0 0 1.8em 2.2em;
    border: 1px solid #ccc;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.12);
  }

  @media (max-width: 850px) {
    .wrapper {
      flex-direction: column;
      gap: 35px;
    }
    .sidebar {
      width: 100%;
    }
    .profile-photo {
      float: none;
      display: block;
      margin: 0 auto 1.8em;
    }
  }
</style>