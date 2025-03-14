mod days;
use days::day1;

fn main() {
    let input: &str = "input/day1.txt";
    println!("Day 1 part 1: {}", day1::part1(input));
    println!("Day 1 part 2: {}", day1::part2(input));
}