{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [
    awscli2
    unzip
    pv
    ghostscript_headless
    libreoffice
  ];
  languages.python = {
    enable = true;
    venv.enable = true;
    version = "3.11"; # Required for awscli2
    uv.enable = true;
  };
  dotenv.enable = true;
  enterShell = ''
    uv pip install -r requirements.txt
    clear
  '';
  scripts.clean.exec = "rm -rf downloads extracted_files supported_files pdf_page_counts_supported_files.json";
}
