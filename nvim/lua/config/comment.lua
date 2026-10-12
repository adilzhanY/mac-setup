require('Comment').setup({
    -- Hook to be ran before commenting.
    --
    -- The hook receives a context object `ctx` that contains information about the comment operation.
    --
    -- The `pre_hook` can be used to dynamically change the commentstring.
    --
    -- For more information see: https://github.com/numToStr/Comment.nvim/wiki/Configuration#pre_hook
    pre_hook = function(ctx)
        -- Only perform this hook on block comments
        if ctx.type == 'block' then
            local U = require('Comment.utils')

            -- Get the location of the cursor
            local location = nil
            if ctx.cmotion == U.cmotion.visual then
                location = U.get_visual_start_location()
            else
                location = U.get_cursor_location()
            end

            -- Check if the cursor is inside a JSX element
            local is_jsx = U.is_ts_node(
                { 'jsx_element', 'jsx_self_closing_element', 'jsx_fragment' },
                location.row,
                location.col
            )

            -- If it is a JSX element, use the JSX comment string
            if is_jsx then
                ctx.custom_commentstring = '{/*%s*/}'
            end
        end
    end,
})