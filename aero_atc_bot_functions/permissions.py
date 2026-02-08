from discord import app_commands, Interaction, Member
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Using sets for O(1) lookups
class RoleIDs:
    AMBASSADOR = {config["aeroPermissions"]["ambassador"]}
    DIRECTOR = {config["aeroPermissions"]["ambassador"], config["aeroPermissions"]["director"]}
    MANAGER = {config["aeroPermissions"]["ambassador"], config["aeroPermissions"]["director"],
               config["aeroPermissions"]["manager"]}
    ATC_STAFF = {config["aeroPermissions"]["atc_staff"]}
    EVENT_HOST = {config["aeroPermissions"]["event_host"]}
    CONTROLLER = {config["aeroPermissions"]["controller"]}
    VERIFIED = {config["aeroPermissions"]["verified"]}

def has_role(required_role: set, admin_bypass: bool = False):
    async def predicate(ctx: Interaction) -> bool:
        if not isinstance(ctx.user, Member):
            await ctx.response.send_message("This command must be used in a server", ephemeral=True)
            return False
        
        # If a command has the admin bypass enabled, any admin can run it regardless of other roles
        # The admin bypass is disabled by default and can be individually toggled for any command
        if admin_bypass and ctx.user.guild_permissions.administrator:
                return True
        
        # Get the IDs of all roles the user currently has
        user_role_ids: set[int] = {role.id for role in ctx.user.roles}
        
        # Check if there is any overlap (intersection) between user roles and required roles
        if not user_role_ids.intersection(required_role):
            await ctx.response.send_message("You do not have permission to run this command", ephemeral=True)
            return False
            
        return True
    return app_commands.check(predicate)