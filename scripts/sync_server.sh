#!/bin/bash
exec bin/minetest --server --world newworld --gameid minetest --sync-port 30010 --sync-dtime 0.1 --config scripts/minetest.conf
