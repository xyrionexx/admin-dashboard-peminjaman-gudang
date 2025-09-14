<script lang="ts">
	import { scaleBand } from 'd3-scale';
	import { BarChart, type ChartContextValue } from 'layerchart';
	import TrendingUpIcon from '@lucide/svelte/icons/trending-up';
	import * as Chart from '$lib/components/ui/chart/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { cubicInOut } from 'svelte/easing';
	import { PieChart } from 'layerchart';

	const chartConfigPeminjaman = {
		jumlah: { label: 'Jumlah', color: '#7dd3fc' }
	} satisfies Chart.ChartConfig;
	let context = $state<ChartContextValue>();

	const chartDataPeminjaman = [
		{ day: 'Senin', jumlah: 186 },
		{ day: 'Selasa', jumlah: 305 },
		{ day: 'Rabu', jumlah: 237 },
		{ day: 'Kamis', jumlah: 73 },
		{ day: 'Jum&#39;at', jumlah: 209 }
	];

	const chartDataSering = [
		{ barang: 'proyektor', jumlah: 275, color: 'var(--color-proyektor)' },
		{ barang: 'speaker', jumlah: 200, color: 'var(--color-speaker)' },
		{ barang: 'terminal', jumlah: 187, color: 'var(--color-terminal)' },
		{ barang: 'laptop', jumlah: 173, color: 'var(--color-laptop)' },
		{ barang: 'other', jumlah: 90, color: 'var(--color-other)' }
	];
	const chartConfigSering = {
		visitors: { label: 'Visitors' },
		proyektor: { label: 'Proyektor', color: '#7dd3fc' }, // biru muda
		speaker: { label: 'Speaker', color: '#38bdf8' }, // biru sedikit lebih tua
		terminal: { label: 'Terminal', color: '#0ea5e9' }, // biru medium
		laptop: { label: 'Laptop', color: '#0284c7' }, // biru tua
		other: { label: 'Other', color: '#0369a1' } // biru lebih tua lagi
	} satisfies Chart.ChartConfig;
</script>

<div class="space-y-6">
	<!-- <div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-900">Analytics</h1>
		<div class="flex space-x-2">
			<select class="rounded-lg border border-gray-300 px-3 py-2 text-sm">
				<option>Last 7 days</option>
				<option>Last 30 days</option>
				<option>Last 90 days</option>
			</select>
		</div>
	</div> -->

	<!-- Chart Placeholder -->
	<div class="flex w-full">
		<Card.Root class="w-full ">
			<Card.Header>
				<Card.Title>Jumlah Peminjaman</Card.Title>
				<Card.Description>Pada Minggu ini</Card.Description>
			</Card.Header>
			<Card.Content class="h-[30vh] w-full">
				<Chart.Container config={chartConfigPeminjaman} class="h-full w-full">
					<BarChart
						bind:context
						data={chartDataPeminjaman}
						xScale={scaleBand().padding(0.25)}
						x="day"
						axis="x"
						series={[{ key: 'jumlah', label: 'Jumlah', color: chartConfigPeminjaman.jumlah.color }]}
						props={{
							bars: {
								stroke: 'none',
								rounded: 'all',
								radius: 8,
								initialY: context?.height,
								initialHeight: 0,
								motion: {
									x: { type: 'tween', duration: 500, easing: cubicInOut },
									width: { type: 'tween', duration: 500, easing: cubicInOut },
									height: { type: 'tween', duration: 500, easing: cubicInOut },
									y: { type: 'tween', duration: 500, easing: cubicInOut }
								}
							},
							highlight: { area: { fill: 'none' } },
							xAxis: { format: (d) => d.slice(0, 3) }
						}}
					>
						{#snippet tooltip()}
							<Chart.Tooltip hideLabel />
						{/snippet}
					</BarChart>
				</Chart.Container>
			</Card.Content>
		</Card.Root>
	</div>

	<div class=" flex w-full gap-5">
		<Card.Root class="flex w-full flex-col">
			<Card.Header class="items-center">
				<Card.Title>Barang Sering Dipinjam</Card.Title>
				<Card.Description>Pada Minggu Ini</Card.Description>
			</Card.Header>
			<Card.Content class="flex-1">
				<Chart.Container config={chartConfigSering} class="mx-auto aspect-square max-h-[250px]">
					<PieChart
						data={chartDataSering}
						key="barang"
						value="jumlah"
						cRange={chartDataSering.map((d) => d.color)}
						c="color"
						props={{
							pie: {
								motion: 'tween'
							}
						}}
					>
						{#snippet tooltip()}
							<Chart.Tooltip hideLabel />
						{/snippet}
					</PieChart>
				</Chart.Container>
			</Card.Content>
		</Card.Root>

		<Card.Root class="flex w-full flex-col">
			<Card.Header class="items-center">
				<Card.Title>Kategori Sering Dipinjam</Card.Title>
				<Card.Description>Pada Minggu Ini</Card.Description>
			</Card.Header>
			<Card.Content class="flex-1">
				<Chart.Container config={chartConfigSering} class="mx-auto aspect-square max-h-[250px]">
					<PieChart
						data={chartDataSering}
						key="barang"
						value="jumlah"
						cRange={chartDataSering.map((d) => d.color)}
						c="color"
						props={{
							pie: {
								motion: 'tween'
							}
						}}
					>
						{#snippet tooltip()}
							<Chart.Tooltip hideLabel />
						{/snippet}
					</PieChart>
				</Chart.Container>
			</Card.Content>
		</Card.Root>
	</div>
</div>
