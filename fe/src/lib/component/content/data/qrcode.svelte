<script lang="ts">
	import { onMount } from 'svelte';

	export let value: string;
	let canvas: HTMLCanvasElement;

	onMount(async () => {
		const QRCode = await import('qrcode');
		await QRCode.toCanvas(canvas, value, { width: 200 });
	});
</script>

<canvas bind:this={canvas}></canvas>
