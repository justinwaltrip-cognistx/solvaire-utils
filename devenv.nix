{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [
    awscli2
    unzip
    pv
  ];
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        boto3
        tqdm
      '';
    };
  };
  dotenv.enable = true;
  enterShell = ''
    clear
  '';
}
