from discord import app_commands, Interaction, Member
from typing import List

# Using sets for O(1) lookups
class RoleIDs:
    DIRECTORS = {1175138965054042212, 1180831972440944750}
    STAFF = {1292556748774838405}
    CONTROLLERS = {1168202336942948393}
    VERIFIED = {1120128265668022292}

def has_any_role(required_role_set: set, admin_bypass: bool = False):

    async def predicate(ctx: Interaction) -> bool:

        if not isinstance(ctx.user, Member):
            await ctx.response.send_message("This command must be used in a server", ephemeral=True)
            return False
        
        # If a command has the admin bypass enabled, any admin can run it regardless of other roles
        # The admin bypass is disabled by default and can be individually toggled for any command
        if admin_bypass:
            if ctx.user.guild_permissions.administrator:
                return True
        
        # Get the IDs of all roles the user currently has
        user_role_ids: set[int] = {role.id for role in ctx.user.roles}
        
        # Check if there is any overlap (intersection) between user roles and required roles
        if not user_role_ids.intersection(required_role_set):
            await ctx.response.send_message("You do not have permission to run this command", ephemeral=True)
            return False
            
        return True
    
    return app_commands.check(predicate)