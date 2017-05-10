# Imitation Project
### Spring 2017 
### CMSC435
### Learn More at our [website](http://viceroy.cs.umd.edu/) 
Team:
Julien Homble,
Ben Mariano,
Kyle Urban,
Derek Farley,
Chris Dear,
Susmitha Yenugula,
David Schlegel,
Amber Mirza

## Purpose
The goal of our project is to design a robust, modular API for rapid configuration of imitation-based simulation experiments using Reggia and Katz’s software in other domains. This will be done by delivering an Electron desltop application that allows the user to input a demonstration of a task they would like to replicate. Our API would then output the various “imitation” situations that the system infers from that task and a start situation. The application includes the capability of creating custom “causal intention relations” from a GUI. These relations are crucial to the imitation algorithm which will now be built for new tasks, rather than the ones Reggia and Katz have been using for their specific block stacking example. From this, we intend to provide an intuitive, visual layout design for configuring new imitation causal intention relations, and remove the need for the user to have to create the corresponding code base for every unique experiment from scratch.  

## Requirements

Electron is no longer a dev dependency and is expected to be installed globally:

```bash
npm install -g electron
```

## To Use

To clone and run this repository you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/jhomble/electron435
# Go into the repository
$ cd electron-angular-boilerplate
# Install dependencies and run the app
$ npm install && npm start
```

Learn more about Electron and its API in the [documentation](http://electron.atom.io/docs/latest).


