{ pkgs, lib, config, inputs, ... }:

{
  packages = [
    pkgs.awscli2
  ];
  dotenv.enable = true;
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
}
