# Roslyn Analyzers Sample

A set of three sample projects that includes Roslyn analyzers with code fix providers. Enjoy this template to learn from and modify analyzers for your own needs.

## Content
### ConsoleApp1saf
A .NET Standard project with implementations of sample analyzers and code fix providers.
**You must build this project to see the results (warnings) in the IDE.**

- [SampleSemanticAnalyzer.cs](SampleSemanticAnalyzer.cs): An analyzer that reports invalid values used for the `speed` parameter of the `SetSpeed` function.
- [SampleSyntaxAnalyzer.cs](SampleSyntaxAnalyzer.cs): An analyzer that reports the company name used in class definitions.
- [SampleCodeFixProvider.cs](SampleCodeFixProvider.cs): A code fix that renames classes with company name in their definition. The fix is linked to [SampleSyntaxAnalyzer.cs](SampleSyntaxAnalyzer.cs).

### ConsoleApp1saf.Sample
A project that references the sample analyzers. Note the parameters of `ProjectReference` in [ConsoleApp1saf.Sample.csproj](../ConsoleApp1saf.Sample/ConsoleApp1saf.Sample.csproj), they make sure that the project is referenced as a set of analyzers. 

### ConsoleApp1saf.Tests
Unit tests for the sample analyzers and code fix provider. The easiest way to develop language-related features is to start with unit tests.

## How To?
### How to debug?
- Use the [launchSettings.json](Properties/launchSettings.json) profile.
- Debug tests.

### How can I determine which syntax nodes I should expect?
Consider using the Roslyn Visualizer toolwindow, witch allow you to observe syntax tree.

### Learn more about wiring analyzers
The complete set of information is available at [roslyn github repo wiki](https://github.com/dotnet/roslyn/blob/main/docs/wiki/README.md).

## Distribution & Licensing
This project is licensed under the MIT License (see LICENSE file). You may use, modify, and sell this analyzer library as permitted by the license.

## GitHub Authentication & CLI Usage
To interact with GitHub (e.g., for publishing, automation, or using GitHub Actions):
- Install the GitHub CLI: https://cli.github.com/
- Authenticate using:
  ```sh
  gh auth login
  ```
- For API access, create a personal access token at https://github.com/settings/tokens and use it as needed.

### Example: Publishing to GitHub
1. Initialize git and commit your code:
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Create a new repository on GitHub and push:
   ```sh
   gh repo create <your-repo-name> --public
   git push -u origin master
   ```

### Example: Using the Analyzer via CLI
If you provide a CLI tool for your analyzer, document its usage here. For example:
```sh
# Run analyzer on a C# project
ConsoleApp1safAnalyzerCli analyze ./MyProject
```

## Support & Contributions
- For issues or feature requests, open an issue on GitHub.
- Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Contact
For commercial licensing, support, or custom development, contact: <your-email-or-website>
