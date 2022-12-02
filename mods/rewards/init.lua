reward_channels = {}

function get_channel(player)
    return "reward"..player:get_nametag_attributes().text
end

minetest.register_on_joinplayer(function(player, _)
    local channel = get_channel(player)
    reward_channels[channel] = minetest.mod_channel_join(channel)
end)

minetest.register_on_player_hpchange(function(player, hp_change, reason)
    local channel = get_channel(player)
    reward_channels[channel]:send_all(hp_change)
end)

-- minetest.register_globalstep(function()
--     for _, player in pairs(minetest.get_connected_players()) do

--     end
-- end)
