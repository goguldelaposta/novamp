use tauri::Emitter;
use tauri_plugin_updater::UpdaterExt;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

// Called from JS once the frontend is ready; fires update check and emits progress events.
#[tauri::command]
fn check_update(app: tauri::AppHandle) {
    tauri::async_runtime::spawn(async move {
        do_update(app).await;
    });
}

async fn do_update(app: tauri::AppHandle) {
    let updater = match app.updater() {
        Ok(u) => u,
        Err(_) => {
            let _ = app.emit("update-not-available", ());
            return;
        }
    };

    match updater.check().await {
        Ok(Some(update)) => {
            let _ = app.emit("update-available", &update.version);
            let mut downloaded: u64 = 0;
            let app1 = app.clone();
            let app2 = app.clone();
            let result = update
                .download_and_install(
                    move |chunk, total| {
                        downloaded += chunk as u64;
                        let pct = total
                            .map(|t| (downloaded as f64 / t as f64) * 100.0)
                            .unwrap_or(50.0);
                        let _ = app1.emit("update-progress", pct);
                    },
                    move || {
                        let _ = app2.emit("update-installing", ());
                    },
                )
                .await;
            if result.is_ok() {
                app.restart();
            } else {
                let _ = app.emit("update-not-available", ());
            }
        }
        Ok(None) => {
            let _ = app.emit("update-not-available", ());
        }
        Err(_) => {
            let _ = app.emit("update-not-available", ());
        }
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .invoke_handler(tauri::generate_handler![greet, check_update])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
