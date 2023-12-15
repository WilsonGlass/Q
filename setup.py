from setuptools import setup

setup(
    name = "proj-directory",
    version = "0.0.1",
    description = ("The Q Game details"),
    packages=['Q',
              'Q.Common',
              'Q.Common.Board',
              'Q.Common.Turn',
              'Q.Player.Strategy.Cheat',
              'Q.Player',
              'Q.Player.Strategy',
              'Q.Referee',
              'Q.Tests',
              'Q.Util',
              'Q.Server',
              'Q.Client',
              'Q.Common.RefereeMethods',
              'Q.Util.Configurations'
              ],
)