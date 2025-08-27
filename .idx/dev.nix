{ pkgs, ... }: {
  # See https://developers.google.com/idx/guides/customize-idx-env#nix-files
  # for more details on customizing your environment with Nix.
  channel = "stable-23.11";
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.grpc-tools
    pkgs.python311Packages.grpcio-tools
    pkgs.docker
    pkgs.docker-compose
    pkgs.gh
  ];

  idx = {
    extensions = [
      "ms-python.python"
      "ms-python.debugpy"
      "zxh404.vscode-proto3"
      "PKief.material-icon-theme"
    ];
  };

  services.docker.enable = true;
}
