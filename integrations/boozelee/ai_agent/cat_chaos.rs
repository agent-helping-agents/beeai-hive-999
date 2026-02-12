use std::io::{self, Write};
use rand::Rng;

fn main() {
    let moods = vec!["😾", "🐱", "😸", "🙀", "🐈‍⬛"];
    println!("🐱 RUST CAT CHAOS 🐱");
    
    loop {
        print!("Paw> ");
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let input = input.trim();
        
        if input == "quit" { break }
        
        let mut rng = rand::thread_rng();
        let mood = &moods[rng.gen_range(0..moods.len())];
        let chaos = rng.gen_range(1..11);
        
        println!("🐾 {} 🐾", input.to_uppercase());
        println!("RustCat: {} -> CHAOS {} {}", 
                 input.chars().rev().collect::<String>(), chaos, mood);
    }
}
