import os, subprocess, sys, venv
for name in ["venv-short", "test.test_sysconfig.TestSysConfig.test_config_vars_depend_on_site_initialization-venv-abcdefgh"]:
    d = os.path.join(os.getcwd(), "diag", name)
    venv.EnvBuilder(with_pip=False, symlinks=True).create(d)
    exe = os.path.join(d, "bin", "python")
    print("== len", len(exe), "islink", os.path.islink(exe), os.path.realpath(exe))
    for env_name, env in [("inherited", dict(os.environ)), ("no PYTHONHOME", {k: v for k, v in os.environ.items() if k != "PYTHONHOME"})]:
        for args in (["-c", "import sysconfig, sys; print(sys.prefix)"], ["-S", "-c", "import sysconfig, sys; print(sys.prefix)"]):
            r = subprocess.run([exe, *args], env=env, capture_output=True, text=True)
            print(f"-- {env_name} {args[0]}: rc={r.returncode}\nstdout={r.stdout.strip()}\nstderr={r.stderr.strip()[-1500:]}")
