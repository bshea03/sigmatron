import { redirect } from "next/navigation";
import { getServerSession } from "next-auth";
import { authOptions } from "../../auth";

export default async function DashboardPage() {
    const session = await getServerSession(authOptions);

    if (!session) redirect("/");

    return (
        <main>
            <h1>Dashboard</h1>
            <p>Welcome, {session.toString()}</p>
        </main>
    );
}