#!/bin/bash
protoc -I=proto/ --python_out=minetester/proto --cpp_out=src proto/*.proto
