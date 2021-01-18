const typewriter = new Typewriter('#typewriter', {
  loop: true,
  delay: 80,
  deleteSpeed: 2
});

typewriter.typeString('Hello World, soy H. Ulises G.M.  ')
  .typeString('un programador ')
  .typeString('Frontend 💻')
  .pauseFor(1000)
  .deleteChars(11)
  .typeString('Backend 🖥')
  .pauseFor(1000)
  .deleteChars(26)
  .typeString('Music Lover ❤️')
  .pauseFor(1000)
  .deleteChars(14)
  //
  .typeString('Bloguero casual ✍')
  .pauseFor(1000)
  .deleteChars(17)
  //
  .typeString('Sensei 🏷')
  .pauseFor(1000)
  .deleteChars(9)
  .typeString('Miembro de comunidad 🙋')
  .pauseFor(1000)
  .deleteChars(23)
  .pauseFor(1000)
  .start();