import { IoLogoDiscord } from "react-icons/io5";
import { Button } from "./ui/button";
import { auth, signIn } from "@/auth";

export async function DiscordLoginButton({}) {
  const session = await auth();

  return (
    <form
      action={async () => {
        "use server";
        await signIn("discord", { redirectTo: "/dashboard" });
      }}
    >
      <Button type="submit" variant="outline" className="h-14">
        <IoLogoDiscord className="size-8 mr-1" />
        Log in with Discord
      </Button>
    </form>
  );
}
