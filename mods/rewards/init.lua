minetest.register_globalstep(function()
    for _, player in pairs(minetest.get_connected_players()) do
        local hp = player:get_hp()
        player:get_meta():set_float("reward", hp)
        print(hp)
    end
end)
