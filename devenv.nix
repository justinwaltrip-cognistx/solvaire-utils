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
  };
  dotenv.enable = true;
  enterShell = ''
    clear
  '';
}
