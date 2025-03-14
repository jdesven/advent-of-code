use std::fs;

pub fn part1(path: &str) -> usize {
    let input: String = fs::read_to_string(path).unwrap();
    fn count_chars(input: &str, char_search: char) -> usize {
        String::from(input)
            .chars()
            .filter(|c: &char|*c == char_search)
            .count()
    }
    count_chars(&input, '(') - count_chars(&input, ')')
}

pub fn part2(path: &str) -> usize {
    let input: String = fs::read_to_string(path).unwrap();
    let mut pos: i32 = 0;
    for (i, char) in input.chars().enumerate() {
        match char {
            '(' => pos += 1,
            ')' => pos -= 1,
            _ => panic!("disallowed character encountered")
        }
        if pos < 0 {
            return i + 1
        }
    }
    panic!("basement is never reached")
}