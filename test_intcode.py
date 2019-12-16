#!/usr/bin/env python3
import pexpect


def main():
    """
    Run all previous intcode answers that uses our new intcode machine and validate
    that the output is correct. Sadly I won't rewrite my old answers to use the current code.
    """
    wrapper = "./venv/bin/python3 {}"

    print("Test: day5_part2.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day5_part2.py"))
    child.expect("Please give an input: ", timeout=5)
    child.sendline("5")
    child.expect("7873292")
    child.expect(pexpect.EOF)
    print("Passed")

    print("Test: day7_part1.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day7_part1.py"))
    child.expect("34852")
    child.expect(pexpect.EOF)
    print("Passed")

    print("Test: day7_part2.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day7_part2.py"))
    child.expect("44282086")
    child.expect(pexpect.EOF)
    print("Passed")

    print("Test: day9_part1.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day9_part1.py"))
    child.expect("Please give an input: ", timeout=5)
    child.sendline("1")
    child.expect("4080871669")
    child.expect(pexpect.EOF)
    print("Passed")

    print("Test: day9_part2.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day9_part2.py"))
    child.expect("Please give an input: ", timeout=5)
    child.sendline("2")
    child.expect("75202")
    child.expect(pexpect.EOF)
    print("Passed")

    print("Test: day13_part1.py ... ", end="")
    child = pexpect.spawn(wrapper.format("day13_part1.py"))
    child.expect("277", timeout=5)
    child.expect(pexpect.EOF)
    print("Passed")

    print("All done.")


if __name__ == '__main__':
    main()
