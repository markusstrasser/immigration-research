"""Insert the estimates tables into section 3 of the memo, replacing whatever is there."""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
MEMO = pathlib.Path("/Users/alien/Projects/immigration-research/research/"
                    "immigration-employment-entry-displacement-2026-09-18.md")
START = "## 3. Estimates"
END = "## 4. What this design does and does not identify"


def main():
    tables = (HERE / "derived" / "tables.md").read_text()
    body = sys.stdin.read() if not sys.stdin.isatty() else ""
    s = MEMO.read_text()
    i, j = s.index(START), s.index(END)
    new = START + "\n\n" + (body.strip() + "\n\n" if body.strip() else "") + tables.strip() + "\n\n"
    MEMO.write_text(s[:i] + new + s[j:])
    print("memo section 3 rewritten,", len(tables), "chars of tables")


if __name__ == "__main__":
    main()
