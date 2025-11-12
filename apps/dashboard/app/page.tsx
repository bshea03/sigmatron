import { DiscordLoginButton } from "@/components/DiscordLoginButton";
import { auth } from "@/auth";

export default async function Home() {
  let isAuthenticated = await auth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      {!isAuthenticated ? <DiscordLoginButton /> : null}
    </div>
  );
}
