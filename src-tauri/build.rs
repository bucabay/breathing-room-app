fn main() {
    use base64::Engine;
    let root=std::path::PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap()).parent().unwrap().to_path_buf();
    let template=root.join("public/auth-return.html");
    println!("cargo:rerun-if-changed={}",template.display());
    let mut fonts=String::new();
    for (family,path,weight) in [
        ("DM Sans","node_modules/@fontsource/dm-sans/files/dm-sans-latin-400-normal.woff2",400),
        ("Space Grotesk","node_modules/@fontsource/space-grotesk/files/space-grotesk-latin-600-normal.woff2",600),
    ] {
        let path=root.join(path);println!("cargo:rerun-if-changed={}",path.display());
        if let Ok(bytes)=std::fs::read(path){let encoded=base64::engine::general_purpose::STANDARD.encode(bytes);fonts.push_str(&format!("@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;src:url(data:font/woff2;base64,{encoded}) format('woff2');}}\n"));}
    }
    let html=std::fs::read_to_string(template).expect("Sign-in page template unavailable").replace("{{font_faces}}",&fonts);
    std::fs::write(std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("auth-return.html"),html).expect("Could not bundle sign-in page");
    #[cfg(feature = "gui")]
    tauri_build::build();
}
