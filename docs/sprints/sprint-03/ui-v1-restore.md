# Restoring website UI v1

The **v1** look (neutral system UI) is frozen at Git tag **`website-v1`**.

- **Full tree at v1:** `git checkout website-v1` (detached) or create a branch from the tag.
- **Stylesheet only:** `git show website-v1:static/style.css` or copy from `static/style-v1-baseline.css` in the current tree.

After restoring `static/style.css`, revert template changes from the same tag if you need the exact v1 HTML structure:

`git checkout website-v1 -- templates/ static/style.css`
