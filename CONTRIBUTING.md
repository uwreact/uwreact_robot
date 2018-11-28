# Contributing Guide

Thank you for your interest in contributing to this project! We're excited to work with you.

Please review the entirety of this document before opening an issue or submitting a pull request; doing so ensures the process is easy and effective for everyone involved.

## Getting Started with UW REACT

This project is just one of many autonomous robotics endeavours undertaken by UW REACT.

### What is UW REACT?

The [University of Waterloo Robotics Engineering and Autonomous Controls Team (UW REACT)](https://uwreact.ca) is a student design team composed primarily of undergraduate students at the University of Waterloo. We design, manufacture, program, and train fully autonomous FIRST Robotics Competition (FRC) robots. We field a new robot each year to compete against high school FRC teams without using a human driver.

### How can I help?

Depending on your situation, there are two main ways to collaborate:

- **Like normal:** Just like any open source team, we maintain an active issue tracker and review pull requests as often as possible, allowing anyone to collaborate on GitHub.
- **Join our team:** If you are a student at the University of Waterloo, you can [apply to join our core team](https://uwreact.ca/apply) to gain access to Slack and push permissions to this repository.

### Opening Issues

The [issue tracker](https://github.com/uwreact/shire/issues) is our preferred method for reporting bugs and suggesting features. We ask that you:

- **DO** check if a similar issue has already been reported.
- **DO** follow the issue templates for the type of issue you are opening.
- **DO** label the issue with the labels specified in the template.
- **DO NOT** use the issue tracker for personal support requests. Email [hello@uwreact.ca](mailto:hello@uwreact.ca).
- **DO NOT** derail or troll issues. Keep discussion on topic.
- **DO NOT** post '+1' or '👍' comments. Use GitHub reactions for this.

### Submitting Pull Requests

Never embark on a pull request before selecting an issue to solve. If no similar issue exists, please open one first and wait for feedback before proceeding. If you submit a pull request that does not address an open issue, you may spend a lot of time writing changes that we may not merge into the project.

The easiest way to get started once you've selected an issue is:

1. [Fork the project](https://help.github.com/articles/fork-a-repo/).

2. Clone your fork:

```bash
git clone https://github.com/<your-username>/shire.git
```

3. Configure your remotes:

```bash
git remote add upstream https://github.com/uwreact/shire.git
```

4. Get the latest changes:

```bash
git checkout master
git pull upstream master
```

5. Create a new branch off of `master`:

```bash
git checkout -b <branch-name>
```

6. Commit your changes.

7. Locally merge the upstream branch into your branch:

```bash
git pull upstream master
```

8. [Open a pull request](https://help.github.com/articles/about-pull-requests/)

### Good First Issues

If you're not sure where to start, we maintain a list of [good first issues](https://github.com/uwreact/shire/labels/good%20first%20issue) with a limited scope for each of our projects.

## Getting Started with this project

These instructions will set up your local machine for developing, testing, and deploying this project.

### Prerequisites

Install [Yarn](https://yarnpkg.com/en/) on your machine.

Create a project on [Firebase](https://firebase.google.com/) and copy the configuration variables into `merry/.env.development`.

Create an application on the [Microsoft Application Registration Portal](https://apps.dev.microsoft.com/portal/register-app) and copy the ID into `pippin/.env.developmnent`.

### Installation

Install dependencies using yarn:

```bash
yarn
```

### Development

Start the application with webpack development server:

```bash
cd merry
yarn start
```

### Testing

Test the application with jest:

```bash
cd [merry/pippin]
yarn test
```

### Deployment

Modify `[merry/pippin]/package.json` to include your Firebase project,
then deploy the application to your Firebase project:

```bash
cd [merry/pippin]
yarn deploy
```
