<script setup>
import Spinner from "../components/Spinner.vue";
import { pb } from "../pocketbase.js";

console.log("what", localStorage.getItem("access_token"));

const UpdateUserData = async () => {
	const userResponse = await fetch("https://discord.com/api/v10/users/@me", {
		headers: {
			Authorization: `Bearer ${localStorage.getItem("access_token")}`,
		},
	});
	const userData = await userResponse.json();

	await pb.collection("users").update(pb.authStore.model.id, {
		global_name: userData.global_name,
		avatar_url: `https://cdn.discordapp.com/avatars/${userData.id}/${userData.avatar}`,
		discord_id: userData.id,
		banner: userData.banner
			? `https://cdn.discordapp.com/banners/${userData.id}/${userData.banner}`
			: null,
		banner_color: userData.banner_color,
	});
};

const Login = async () => {
	const authData = await pb.collection("users").authWithOAuth2({
		provider: "discord",
		// redirectUrl:
		// 	"https://discord.com/api/v10/oauth2/authorize?client_id=1128066454768599100&redirect_uri=http%3A%2F%2F157.245.244.129%2Fapi%2Foauth2-redirect&response_type=code&scope=identify%20email%20connections%20guilds%20guilds.members.read",
		createData: {
			permissions: "member",
		},
	});

	const discordData = await authData.meta.rawUser;
	console.log(authData.meta);

	await pb.collection("users").update(pb.authStore.model.id, {
		global_name: discordData.global_name,
		avatar_url: authData.meta.avatarUrl,
		discord_id: discordData.id,
		banner: discordData.banner
			? `https://cdn.discordapp.com/banners/${discordData.id}/${discordData.banner}`
			: null,
		banner_color: discordData.banner_color,
	});

	localStorage.setItem("access_token", authData.meta.accessToken);
	localStorage.setItem("refresh_token", authData.meta.refreshToken);
};

const SyncData = async () => {
	try {
		await UpdateUserData();
	} catch (e) {
		if (e.message == "401: Unauthorized") {
			try {
				const tokenResponse = await fetch(
					"https://discord.com/api/oauth2/token",
					{
						method: "POST",
						headers: {
							"Content-Type": "application/x-www-form-urlencoded",
						},
						body: new URLSearchParams({
							client_id: import.meta.env.CLIENT_ID,
							client_secret: import.meta.env.CLIENT_SECRET,
							grant_type: "refresh_token",
							refresh_token: localStorage.getItem("refresh_token"),
						}),
					},
				);
				const tokenData = await tokenResponse.json();

				await localStorage.setItem("access_token", tokenData.access_token);
				await localStorage.setItem("refresh_token", tokenData.refresh_token);

				await UpdateUserData();
			} catch (e) {
				alert(e);
			}
		} else {
			alert("Unknown error occurred", e);
		}
	}
};
</script>

<template>
	<main v-if="loading">
		<Spinner></Spinner>
	</main>
	<main v-else>
		<button class="Login" @click="Login">Login with Discord OAuth2</button>
		<button class="SyncData" @click="SyncData">
			Sync Discord Profile Data
		</button>
	</main>
</template>

<style>
.Login {
	background-color: teal;
}
.SyncData {
	background-color: purple;
}
</style>
