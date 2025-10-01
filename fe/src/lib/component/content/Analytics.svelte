<script lang="ts">
	import { scaleBand } from 'd3-scale';
	import { BarChart, type ChartContextValue } from 'layerchart';
	import TrendingUpIcon from '@lucide/svelte/icons/trending-up';
	import * as Chart from '$lib/components/ui/chart/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { cubicInOut } from 'svelte/easing';
	import { PieChart } from 'layerchart';
	import { onMount } from 'svelte';

	interface Peminjaman {
		kode_pinjam: string;
		tanggal_pinjam: string;
		tanggal_kembali: string;
		status_pinjam: string;
		nis: string | null;
		nuptk: string | null;
		id_pegawai: string | null;
	}

	//untuk grafik data peminjaman

	let context: ChartContextValue;

	interface ChartData {
		day: string;
		jumlah: number;
	}

	const hariIndonesia = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'];

	let chartDataPeminjaman: ChartData[] = [];
	let chartConfigPeminjaman = {
		jumlah: { color: '#7dd3fc' }
	} satisfies Chart.ChartConfig;

	//di bagian bwah untuk data pie chart barang yang sering di pinjam
	interface DetailPeminjaman {
		kode_detail: string;
		id_peminjaman: string;
		id_barang: string;
		jumlah: number;
	}

	interface Barang {
		id_barang: string;
		nama_barang: string;
		kategori?: string; // Add kategori property as optional
	}

	const warnaPie = [
		'#bfdbfe', // biru sangat muda
		'#93c5fd', // biru muda
		'#60a5fa', // biru sedang
		'#3b82f6', // biru normal
		'#2563eb', // biru agak tua
		'#1d4ed8', // biru tua
		'#1e40af', // biru lebih tua
		'#1e3a8a' // biru paling tua
	];

	let chartDataBarang: { name: string; jumlah: number; color: string }[] = [];

	let chartConfigBarang = {
		jumlah: { color: '#7dd3fc' }
	} satisfies Chart.ChartConfig;

	onMount(async () => {
		try {
			console.log('Starting API fetch operations...');
			console.log('Fetching peminjaman data...');
			const res = await fetch('https://api.borrowfy.site/api/peminjaman/');
			if (!res.ok)
				throw new Error(
					'Gagal mengambil data peminjaman: ' + res.statusText + ' (Status: ' + res.status + ')'
				);
			const data: Peminjaman[] = await res.json();
			console.log('Peminjaman data received:', data.length, 'items');

			chartDataPeminjaman = hariIndonesia.map((hari) => {
				const jumlah = data.filter((row) => {
					const dayName = new Date(row.tanggal_pinjam).toLocaleDateString('id-ID', {
						weekday: 'long'
					});
					return dayName.toLowerCase() === hari.toLowerCase();
				}).length;

				return { day: hari, jumlah };
			});

			// Fetch data detail peminjaman untuk pie chart
			console.log('Fetching detail peminjaman data...');
			const resDetail = await fetch('https://api.borrowfy.site/api/detail/peminjaman');
			if (!resDetail.ok)
				throw new Error(
					'Gagal mengambil detail peminjaman: ' +
						resDetail.statusText +
						' (Status: ' +
						resDetail.status +
						')'
				);
			const detail: DetailPeminjaman[] = await resDetail.json();
			console.log('Detail peminjaman data received:', detail.length, 'items');

			// Fetch data barang untuk pie chart
			console.log('Fetching barang data...');
			const resBarang = await fetch('https://api.borrowfy.site/api/barang/');
			if (!resBarang.ok)
				throw new Error(
					'Gagal mengambil data barang: ' +
						resBarang.statusText +
						' (Status: ' +
						resBarang.status +
						')'
				);
			const listBarang: Barang[] = await resBarang.json();
			console.log('Barang data received:', listBarang.length, 'items');

			// Hanya lanjut jika ada detail peminjaman
			if (detail && detail.length > 0) {
				// group by id_barang
				const grouped: Record<string, number> = {};
				for (const d of detail) {
					if (d.id_barang) {
						// Make sure id_barang exists
						grouped[d.id_barang] = (grouped[d.id_barang] || 0) + d.jumlah;
					}
				}

				// map ke format chart - only if we have data
				if (Object.keys(grouped).length > 0) {
					console.log('Creating chart data from grouped data...');

					// Sort by frequency to ensure consistent color assignment (most borrowed items get lighter blue)
					const sortedEntries = Object.entries(grouped).sort(
						(a, b) => (b[1] as number) - (a[1] as number)
					);

					chartDataBarang = sortedEntries.map(([kode, total], idx) => {
						const b = listBarang.find((x) => x.id_barang === kode);
						const barangName = b ? b.nama_barang : kode;

						// Use a consistent color from warnaPie based on the index
						const colorIndex = idx % warnaPie.length;
						const pieColor = warnaPie[colorIndex];

						console.log(
							`Item: ${barangName}, Jumlah: ${total}, Color: ${pieColor} (index: ${colorIndex})`
						);

						return {
							name: barangName,
							jumlah: total,
							color: pieColor
						};
					});

					// Debug: Check if data is loaded correctly
					console.log('Detail Peminjaman:', detail);
					console.log('Barang:', listBarang);
					console.log('Grouped data:', grouped);
					console.log('Chart data:', chartDataBarang);

					// Process kategori data from detail peminjaman and barang
					const kategoriCounts: Record<string, number> = {};

					// Iterate through each detail peminjaman
					for (const d of detail) {
						if (d.id_barang) {
							// Find the corresponding barang to get its kategori
							const barang = listBarang.find((b) => b.id_barang === d.id_barang);

							if (barang && barang.kategori) {
								// Count the occurrences of each kategori
								kategoriCounts[barang.kategori] = (kategoriCounts[barang.kategori] || 0) + d.jumlah;
							} else {
								// If no kategori found, count as 'Lainnya'
								kategoriCounts['Lainnya'] = (kategoriCounts['Lainnya'] || 0) + d.jumlah;
							}
						}
					}

					console.log('Kategori counts:', kategoriCounts);

					// Transform kategori counts to chart data
					if (Object.keys(kategoriCounts).length > 0) {
						// Sort by frequency (most borrowed first)
						const sortedKategori = Object.entries(kategoriCounts).sort((a, b) => b[1] - a[1]);

						chartDataSering = sortedKategori.map(([kategori, jumlah], idx) => {
							// Use predefined color if available, otherwise use from default colors
							const color =
								kategoriColors[kategori] ||
								defaultKategoriColors[idx % defaultKategoriColors.length];

							return {
								barang: kategori,
								jumlah,
								color
							};
						});

						console.log('Kategori chart data:', chartDataSering);
					} else {
						console.warn('No kategori data available');
						// Add sample data when no kategori data is available
						chartDataSering = [{ barang: 'No Data', jumlah: 1, color: '#cccccc' }];
					}
				} else {
					console.warn('No grouped data for pie chart');
					// Add sample data if no data is available
					chartDataBarang = [{ name: 'No Data', jumlah: 1, color: '#cccccc' }];
				}
			} else {
				console.warn('No detail data for pie chart');
				// Add sample data if no data is available
				chartDataBarang = [{ name: 'No Data', jumlah: 1, color: '#cccccc' }];
			}
		} catch (err) {
			// Detailed error logging to help diagnose the issue
			if (err instanceof TypeError && err.message.includes('fetch')) {
				console.error(
					'Network error: Tidak dapat terhubung ke API server. Pastikan server backend berjalan di port 8000:',
					err
				);
			} else if (err instanceof Error) {
				console.error('Error fetch API:', err.name, err.message);
			} else {
				console.error('Gagal fetch API:', err);
			}

			// Check API connection
			fetch('http://127.0.0.1:8000')
				.then((res) => {
					console.log('API server connection status:', res.status, res.statusText);
				})
				.catch((connErr) => {
					console.error('API server is not reachable:', connErr.message);
				});

			// Add sample data if an error occurs
			chartDataBarang = [{ name: 'Error', jumlah: 1, color: '#ff0000' }];
			chartDataSering = [{ barang: 'Error', jumlah: 1, color: '#ff0000' }];
		}
	});

	// Define colors for different categories
	const kategoriColors: { [key: string]: string } = {
		Elektronik: '#7dd3fc', // Light blue
		'Alat Tulis': '#38bdf8', // Medium blue
		'Alat Lab': '#0ea5e9', // Bright blue
		Furniture: '#0284c7', // Dark blue
		Lainnya: '#075985' // Very dark blue
	};

	// Create default colors for any additional categories
	const defaultKategoriColors = [
		'#bfdbfe',
		'#93c5fd',
		'#60a5fa',
		'#3b82f6',
		'#2563eb',
		'#1d4ed8',
		'#1e40af',
		'#1e3a8a'
	];

	// Initialize kategori data
	let chartDataSering: { barang: string; jumlah: number; color: string }[] = [];

	let chartConfigSering = {
		jumlah: { color: '#7dd3fc' }
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
		<Card.Root class="w-full">
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
				{#if chartDataBarang.length > 0 && chartDataBarang[0].name !== 'No Data' && chartDataBarang[0].name !== 'Error'}
					<Chart.Container config={chartConfigBarang} class="mx-auto aspect-square max-h-[250px]">
						<PieChart
							data={chartDataBarang}
							key="name"
							value="jumlah"
							cRange={chartDataBarang.map((d) => d.color)}
							c="color"
							props={{
								pie: {
									motion: 'tween',
									cornerRadius: 3,
									padAngle: 0.02
								}
							}}
						></PieChart>
					</Chart.Container>

					<!-- Legend for the chart -->
					<div class="mt-4 max-h-[150px] overflow-y-auto">
						<table class="w-full text-sm">
							<thead>
								<tr>
									<th class="text-left">Nama Barang</th>
									<th class="text-right">Jumlah</th>
									<th class="text-right">Persentase</th>
								</tr>
							</thead>
							<tbody>
								{#each chartDataBarang as item}
									{@const total = chartDataBarang.reduce((sum, current) => sum + current.jumlah, 0)}
									{@const percentage = ((item.jumlah / total) * 100).toFixed(1)}
									<tr>
										<td>
											<div class="flex items-center gap-2">
												<div
													class="h-3 w-3 rounded-full"
													style="background-color: {item.color}"
												></div>
												<span>{item.name}</span>
											</div>
										</td>
										<td class="text-right">{item.jumlah}</td>
										<td class="text-right">{percentage}%</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{:else if chartDataBarang[0]?.name === 'Error'}
					<div class="flex h-full items-center justify-center">
						<p class="text-destructive text-center">Terjadi kesalahan saat memuat data.</p>
					</div>
				{:else}
					<div class="flex h-full items-center justify-center">
						<p class="text-muted-foreground text-center">Belum ada data peminjaman barang.</p>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>

		<Card.Root class="flex w-full flex-col">
			<Card.Header class="items-center">
				<Card.Title>Kategori Sering Dipinjam</Card.Title>
				<Card.Description>Pada Minggu Ini</Card.Description>
			</Card.Header>
			<Card.Content class="flex-1">
				{#if chartDataSering.length > 0 && chartDataSering[0].barang !== 'No Data' && chartDataSering[0].barang !== 'Error'}
					<Chart.Container config={chartConfigSering} class="mx-auto aspect-square max-h-[250px]">
						<PieChart
							data={chartDataSering}
							key="barang"
							value="jumlah"
							cRange={chartDataSering.map((d) => d.color)}
							c="color"
							props={{
								pie: {
									motion: 'tween',
									cornerRadius: 3,
									padAngle: 0.02
								}
							}}
						></PieChart>
					</Chart.Container>

					<!-- Legend for the chart -->
					<div class="mt-4 max-h-[150px] overflow-y-auto">
						<table class="w-full text-sm">
							<thead>
								<tr>
									<th class="text-left">Nama Kategori</th>
									<th class="text-right">Jumlah</th>
									<th class="text-right">Persentase</th>
								</tr>
							</thead>
							<tbody>
								{#each chartDataSering as item}
									{@const total = chartDataSering.reduce(
										(sum: number, current) => sum + current.jumlah,
										0
									)}
									{@const percentage = ((item.jumlah / total) * 100).toFixed(1)}
									<tr>
										<td>
											<div class="flex items-center gap-2">
												<div
													class="h-3 w-3 rounded-full"
													style="background-color: {item.color}"
												></div>
												<span class="capitalize">{item.barang}</span>
											</div>
										</td>
										<td class="text-right">{item.jumlah}</td>
										<td class="text-right">{percentage}%</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{:else if chartDataSering[0]?.barang === 'Error'}
					<div class="flex h-full items-center justify-center">
						<p class="text-destructive text-center">Terjadi kesalahan saat memuat data kategori.</p>
					</div>
				{:else}
					<div class="flex h-full items-center justify-center">
						<p class="text-muted-foreground text-center">Belum ada data kategori barang.</p>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>
	</div>
</div>
