#!/usr/bin/env bash

VENVNAME=eloenv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME