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
    venv = {
      enable = true;
      requirements = ''
        boto3
        tqdm
        pywin32
        Pillow
        PyPDF2
        tabulate 
        matplotlib 
        seaborn
      '';
    };
    version = "3.11"; # Explicitly specify Python 3.11
  };
  dotenv.enable = true;
  enterShell = ''
    clear
  '';
  scripts.clean.exec = "rm -rf downloads extracted_files supported_files pdf_page_counts_supported_files.json";
}
