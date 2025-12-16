"use client";
import { IoLogoDiscord } from "react-icons/io5";
import { Button } from "./ui/button";
import { signIn, signOut, useSession } from "next-auth/react";

export async function DiscordLoginButton({}) {
  const { data: session } = await useSession();

  const signInCallback = () => {
    signIn("discord", { redirectTo: "/dashboard" });
  }

  const signOutCallback = () => {
    signOut({ redirectTo: "/" });
  }

  return (
    <>
    { session ? (
      <form
        action={signOutCallback}
      >
        <Button type="submit" variant="outline" className="h-14">
          <IoLogoDiscord className="size-8 mr-1" />
          Log out ({session.user?.name ?? "me"})
        </Button>
      </form>
    ) : (
      <form
        action={signInCallback}
      >
        <Button type="submit" variant="outline" className="h-14">
          <IoLogoDiscord className="size-8 mr-1" />
          Log in with Discord
        </Button>
      </form>
    )}
    </>
  );
}
