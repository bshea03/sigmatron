import DiscordProvider from "next-auth/providers/discord";
import type { NextAuthOptions } from "next-auth";

export const authOptions: NextAuthOptions = {
    providers: [
        DiscordProvider({
            clientId: process.env.DISCORD_CLIENT_ID || "",
            clientSecret: process.env.DISCORD_CLIENT_SECRET || "",
            authorization: { params: { scope: "identify guilds" } },
        }),
    ],
    session: { strategy: "jwt" },
    callbacks: {
        async jwt({ token, account, profile }) {
            if (account?.access_token) token.accessToken = account.access_token;
            if (profile?.id) token.id = profile.id;
            return token;
        },
        async session({ session, token }) {
            (session as any).accessToken = (token as any).accessToken;
            (session.user as any).id = (token as any).id;
            return session;
        },
    },
    secret: process.env.NEXTAUTH_SECRET,
};