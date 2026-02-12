use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Style, Stylize},
    widgets::{Block, Borders, List, ListItem, ListState, Paragraph, Gauge},
    Terminal,
};
use crossterm::{
    event::{self, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use serde_json::json;
use std::{io, time::Duration, fs, io::Write};
use chrono::Local;
use mlua::Lua;

const ALIEN_ART: &str = r#"
     .     .  o  .       .  .   . .   .   . .    +  .
  .     .   :      .   .      .   .      .    .
     .   .  |  .      .   .    .    .     .
      .  -- OMNICHANNEL v12 -- .        .           . 
     .   .  |  .      .   .    .    .     .
"#;

async fn log_transmission(content: &str) {
    let date = Local::now().format("%Y-%m-%d").to_string();
    let timestamp = Local::now().format("%H:%M:%S").to_string();
    let filename = format!("logs/session_{}.md", date);
    let mut file = fs::OpenOptions::new().create(true).append(true).open(filename).unwrap();
    writeln!(file, "### [{}] Transmission\n{}\n---\n", timestamp, content).ok();
}

async fn ask_brain(model: &str, prompt: &str, lua: &Lua) -> String {
    let client = reqwest::Client::builder().timeout(Duration::from_secs(120)).build().unwrap();
    
    // Check if prompt is a Lua command: "run: print(1+1)"
    if prompt.starts_with("run:") {
        let code = prompt.strip_prefix("run:").unwrap();
        let func: mlua::Function = lua.globals().get("execute_snippet").expect("Lua engine offline");
        return func.call::<_, String>(code).unwrap_or_else(|e| format!("LUA ERR: {}", e));
    }

    let url = match model {
        m if m.contains("primax") => "https://your-vercel-endpoint.vercel.app/api/chat", // UPDATE THIS
        m if m.contains("brain-x") => "https://api.brain-x.ai/v1/chat",
        _ => "http://127.0.0.1:11434/api/generate",
    };

    let body = if url.contains("11434") {
        json!({ "model": "deepseek-r1:8b", "prompt": prompt, "stream": false })
    } else {
        json!({ "model": model, "messages": [{"role": "user", "content": prompt}] })
    };

    match client.post(url).json(&body).send().await {
        Ok(r) => {
            let json: serde_json::Value = r.json().await.unwrap_or_default();
            let text = json["response"].as_str().or(json["choices"][0]["message"]["content"].as_str()).unwrap_or("RECEPTION ERROR").to_string();
            log_transmission(&format!("Model: {}\nPrompt: {}\nResponse: {}", model, prompt, text)).await;
            text
        },
        Err(_) => "OFFLINE: Check Ollama/Link".to_string(),
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let lua = Lua::new();
    let lua_script = fs::read_to_string("brain_exec.lua").expect("Missing brain_exec.lua");
    lua.load(&lua_script).exec()?;

    enable_raw_mode()?;
    let mut terminal = Terminal::new(CrosstermBackend::new(io::stdout()))?;
    execute!(io::stdout(), EnterAlternateScreen)?;

    let mut history = vec!["[SYSTEM] v12: Omnichannel Link Active.".to_string()];
    let mut input = String::new();
    let mut model_state = ListState::default();
    let installed_models = vec!["deepseek-r1:8b".to_string(), "primax-vercel".to_string(), "brain-x".to_string()];
    model_state.select(Some(0));

    loop {
        let selected_model = &installed_models[model_state.selected().unwrap_or(0)];
        terminal.draw(|f| {
            let chunks = Layout::default().direction(Direction::Horizontal).constraints([Constraint::Percentage(20), Constraint::Percentage(80)]).split(f.size());
            f.render_widget(Block::default().borders(Borders::ALL).title(" 👽 BRAINS "), chunks[0]);
            
            let center = Layout::default().direction(Direction::Vertical).constraints([Constraint::Length(7), Constraint::Min(5), Constraint::Length(3)]).split(chunks[1]);
            f.render_widget(Paragraph::new(ALIEN_ART).green().centered(), center[0]);
            let chat: Vec<ListItem> = history.iter().rev().take(10).rev().map(|h| ListItem::new(h.as_str())).collect();
            f.render_widget(List::new(chat).block(Block::default().borders(Borders::ALL).title(format!(" 📡 ACTIVE: {} ", selected_model))), center[1]);
            f.render_widget(Paragraph::new(input.as_str()).block(Block::default().borders(Borders::ALL).title(" COMMAND (type 'run: <lua>' or chat) ")), center[2]);
        })?;

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                match key.code {
                    KeyCode::Esc => break,
                    KeyCode::Enter => {
                        let msg = input.drain(..).collect::<String>();
                        history.push(format!("You: {}", msg));
                        let resp = ask_brain(selected_model, &msg, &lua).await;
                        history.push(format!("Brain: {}", resp));
                    }
                    KeyCode::Char(c) => input.push(c),
                    KeyCode::Backspace => { input.pop(); }
                    _ => {}
                }
            }
        }
    }
    disable_raw_mode()?;
    execute!(io::stdout(), LeaveAlternateScreen)?;
    Ok(())
}
