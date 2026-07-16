# Contributing to Alpheon

Thanks for taking a look. Alpheon is small and intentionally simple, that's a feature, not a limitation, so contributions that keep it dependency-free and easy to read are especially welcome.

## Reporting issues

Found a bug, or something that doesn't work the way it should?

1. Check [existing issues](../../issues) to see if it's already reported.
2. If not, [open a new issue](../../issues/new) with:
   - What you ran (the exact command)
   - What you expected to happen
   - What actually happened (paste the output if it's short)
   - Your OS and Python version (`python --version`)

Feature ideas are welcome too, open an issue describing the use case, not just the feature.

## Submitting a pull request

1. Fork the repo and create a branch off `main`.
2. Keep changes focused, one logical change per PR is easier to review and merge.
3. Alpheon has no dependencies beyond the Python standard library. Please keep it that way unless there's a very strong reason not to (open an issue to discuss first).
4. Test your change manually against a real git repo with some uncommitted changes, there's no test suite yet, so a clear description of how you verified it helps a lot.
5. Open the PR with a short description of what changed and why (fittingly).

## Code style

Plain, readable Python. No frameworks, no magic. If you can explain a change in one sentence, it's probably the right size.

## Questions

Open an issue, happy to talk through ideas before you write code.
