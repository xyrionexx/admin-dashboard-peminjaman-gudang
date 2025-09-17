<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import * as Pagination from '$lib/components/ui/pagination/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import Icon from '@iconify/svelte';

	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let barangs: any[] = $state([]);
	let search = $state('');
	let value = $state(``);
	let totalStok = $state(0);
	let totalBarang = $state(0);
	let loading = $state(true);
	let currentPage = $state(1);
	const perPage = 10;

	onMount(async () => {
		try {
			const [resData, resSummary] = await Promise.all([
				fetch('http://127.0.0.1:8000/api/barang/'),
				fetch('http://127.0.0.1:8000/api/barang/summary/')
			]);
			if (!resData.ok || !resSummary.ok) {
				throw new Error('Gagal ambil data');
			}
			barangs = await resData.json();
			const summary = await resSummary.json();
			totalStok = summary.total_stok;
			totalBarang = summary.total_barang;
		} catch (err) {
			console.error(err);
		} finally {
			loading = false;
		}
	});

	const categories = $derived([...new Set(barangs.map((b) => b.kategori))]);

	const triggerContent = $derived(
		value ? (categories.find((c) => c === value) ?? 'Semua Kategori') : 'Semua Kategori'
	);

	const filteredBarangs = $derived(
		barangs.filter((b) => {
			const matchCategory = !value || b.kategori === value;
			const matchSearch = !search || b.nama_barang.toLowerCase().includes(search.toLowerCase());
			return matchCategory && matchSearch;
		})
	);

	async function deleteBarang(id: string) {
		if (!confirm('Apakah anda yakin ingin menghapus data ini ?')) return;

		try {
			const res = await fetch(`http://127.0.0.1:8000/api/barang/delete/${id}/`, {
				method: 'DELETE'
			});
			if (!res.ok) {
				throw new Error('Gagal menghapus data');
			}
			barangs = barangs.filter((b) => b.id !== id);

			alert('Data berhasil dihapus');
		} catch (err) {
			console.error(err);
			alert('Terjadi kesalahan saat mengapus data');
		}
	}

	const totalData = $derived(() => filteredBarangs.length);

	const paginatedBarangs = $derived(() => {
		const start = (currentPage - 1) * perPage;
		const end = start + perPage;
		return filteredBarangs.slice(start, end);
	});
</script>

<div class="min-h-screen bg-gray-50 p-4 lg:p-8">
	<div class="mx-auto max-w-7xl">
		<!-- Dashboard Header -->
		<div class="mb-8">
			<div class="mb-6 flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
				<div>
					<h1 class="text-2xl font-semibold text-gray-900 lg:text-3xl">Manajemen Barang</h1>
					<p class="mt-1 text-gray-600">Kelola inventori dan stok barang</p>
				</div>
				<button
					class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 font-medium text-white shadow-sm transition-colors hover:bg-blue-700 lg:px-6"
					onclick={() => dispatch('pageChange', { page: 'TambahBarang' })}
				>
					<Icon icon="mdi:plus" width="20" height="20" />
					Tambah Barang
				</button>
			</div>

			<!-- Dashboard Stats -->
			<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
				<div class="rounded-lg border border-gray-200 bg-white p-6">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
								<Icon icon="mdi:cube-outline" width="24" height="24" class="text-blue-600" />
							</div>
						</div>
						<div class="ml-4">
							<p class="text-sm font-medium text-gray-600">Total Stok</p>
							<p class="text-2xl font-semibold text-gray-900">{totalStok.toLocaleString()}</p>
						</div>
					</div>
				</div>

				<div class="rounded-lg border border-gray-200 bg-white p-6">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
								<Icon icon="mdi:package-variant" width="24" height="24" class="text-green-600" />
							</div>
						</div>
						<div class="ml-4">
							<p class="text-sm font-medium text-gray-600">Total Barang</p>
							<p class="text-2xl font-semibold text-gray-900">{totalBarang.toLocaleString()}</p>
						</div>
					</div>
				</div>

				<div class="rounded-lg border border-gray-200 bg-white p-6">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100">
								<Icon icon="mdi:tag-outline" width="24" height="24" class="text-purple-600" />
							</div>
						</div>
						<div class="ml-4">
							<p class="text-sm font-medium text-gray-600">Kategori</p>
							<p class="text-2xl font-semibold text-gray-900">{categories.length}</p>
						</div>
					</div>
				</div>

				<div class="rounded-lg border border-gray-200 bg-white p-6">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-orange-100">
								<Icon icon="mdi:chart-line" width="24" height="24" class="text-orange-600" />
							</div>
						</div>
						<div class="ml-4">
							<p class="text-sm font-medium text-gray-600">Rata-rata Stok</p>
							<p class="text-2xl font-semibold text-gray-900">
								{totalBarang > 0 ? Math.round(totalStok / totalBarang) : 0}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Data Table Section -->
		<div class="rounded-lg border border-gray-200 bg-white shadow-sm">
			<!-- Table Header with Filters -->
			<div class="border-b border-gray-200 px-6 py-4">
				<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
					<h2 class="text-lg font-semibold text-gray-900">Daftar Barang</h2>

					<!-- Filters -->
					<div class="flex flex-col gap-3 sm:flex-row">
						<div class="min-w-48">
							<Select.Root type="single" name="categoryFilter" bind:value>
								<Select.Trigger class="h-10 w-full border-gray-300 bg-white text-sm">
									<Icon icon="mdi:filter-variant" width="16" height="16" class="mr-2" />
									{triggerContent}
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.Label>Filter Kategori</Select.Label>
										<Select.Item value="">Semua Kategori</Select.Item>
										{#each categories as kategori}
											<Select.Item value={kategori}>{kategori}</Select.Item>
										{/each}
									</Select.Group>
								</Select.Content>
							</Select.Root>
						</div>

						<div class="relative min-w-80">
							<Icon
								icon="mdi:magnify"
								class="absolute left-3 top-1/2 -translate-y-1/2 transform text-gray-400"
								width="16"
								height="16"
							/>
							<input
								type="text"
								placeholder="Cari nama barang..."
								class="h-10 w-full rounded-md border border-gray-300 pl-10 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
								bind:value={search}
							/>
						</div>
					</div>
				</div>
			</div>

			<!-- Mobile Cards View -->
			<div class="block lg:hidden">
				{#if loading}
					<div class="p-6">
						{#each Array(3) as _}
							<div class="border-b border-gray-100 py-4 last:border-b-0">
								<div class="animate-pulse">
									<div class="mb-3 flex items-start justify-between">
										<div class="space-y-2">
											<div class="h-4 w-32 rounded bg-gray-200"></div>
											<div class="h-3 w-20 rounded bg-gray-200"></div>
										</div>
										<div class="h-6 w-6 rounded bg-gray-200"></div>
									</div>
									<div class="flex items-center space-x-3">
										<div class="h-12 w-12 rounded-lg bg-gray-200"></div>
										<div class="space-y-2">
											<div class="h-3 w-16 rounded bg-gray-200"></div>
											<div class="h-3 w-24 rounded bg-gray-200"></div>
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else if paginatedBarangs().length === 0}
					<div class="p-12 text-center">
						<Icon
							icon="mdi:package-variant-closed"
							width="48"
							height="48"
							class="mx-auto mb-4 text-gray-300"
						/>
						<h3 class="mb-2 text-lg font-medium text-gray-900">Tidak ada barang</h3>
						<p class="text-gray-500">
							Barang belum ditambahkan atau tidak sesuai dengan filter pencarian.
						</p>
					</div>
				{:else}
					<div class="divide-y divide-gray-100">
						{#each paginatedBarangs() as b}
							<div class="p-4">
								<div class="mb-3 flex items-start justify-between">
									<div>
										<h3 class="font-medium text-gray-900">{b.nama_barang}</h3>
										<p class="text-sm text-gray-500">ID: {b.id_barang}</p>
									</div>
									<DropdownMenu.Root>
										<DropdownMenu.Trigger class="rounded p-1 hover:bg-gray-100">
											<Icon icon="mdi:dots-vertical" width="20" height="20" class="text-gray-400" />
										</DropdownMenu.Trigger>
										<DropdownMenu.Content>
											<DropdownMenu.Group>
												<DropdownMenu.Label>Aksi</DropdownMenu.Label>
												<DropdownMenu.Separator />
												<DropdownMenu.Item>
													<button
														class="w-full py-1 text-left text-sm"
														onclick={() =>
															dispatch('pageChange', { page: 'Update', id: b.id_barang })}
													>
														Edit Barang
													</button>
												</DropdownMenu.Item>
												<DropdownMenu.Item>
													<button
														class="w-full py-1 text-left text-sm text-red-600"
														onclick={() => deleteBarang(b.id_barang)}
													>
														Hapus Barang
													</button>
												</DropdownMenu.Item>
											</DropdownMenu.Group>
										</DropdownMenu.Content>
									</DropdownMenu.Root>
								</div>

								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										{#if b.img}
											<img
												src={'data:image/png;base64,' + b.img}
												alt={b.nama_barang}
												class="h-12 w-12 rounded-lg border object-cover"
											/>
										{:else}
											<div
												class="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-100"
											>
												<Icon icon="mdi:image" width="20" height="20" class="text-gray-400" />
											</div>
										{/if}
										<div class="space-y-1">
											<div class="flex items-center space-x-4">
												<span class="text-sm text-gray-600"
													>Stok: <span class="font-medium text-gray-900">{b.jumlah}</span></span
												>
												<span
													class="inline-flex items-center rounded bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800"
												>
													{b.kategori}
												</span>
											</div>
											{#if b.deskripsi}
												<p class="line-clamp-1 text-xs text-gray-500">{b.deskripsi}</p>
											{/if}
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<!-- Desktop Table View -->
			<div class="hidden overflow-hidden lg:block">
				<Table.Root>
					<Table.Header>
						<Table.Row class="border-b border-gray-200 bg-gray-50">
							<Table.Head
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								ID Barang
							</Table.Head>
							<Table.Head
								class="py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Nama Barang
							</Table.Head>
							<Table.Head
								class="py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Stok
							</Table.Head>
							<Table.Head
								class="py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Kategori
							</Table.Head>
							<Table.Head
								class="py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Deskripsi
							</Table.Head>
							<Table.Head
								class="py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Gambar
							</Table.Head>
							<Table.Head
								class="py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
							>
								Aksi
							</Table.Head>
						</Table.Row>
					</Table.Header>
					<Table.Body class="divide-y divide-gray-200 bg-white">
						{#if loading}
							{#each Array(perPage) as _}
								<Table.Row>
									<Table.Cell class="px-6 py-4">
										<div class="h-4 w-20 animate-pulse rounded bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4">
										<div class="h-4 w-40 animate-pulse rounded bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4">
										<div class="h-4 w-12 animate-pulse rounded bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4">
										<div class="h-6 w-20 animate-pulse rounded-full bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4">
										<div class="h-4 w-32 animate-pulse rounded bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4">
										<div class="h-12 w-12 animate-pulse rounded-lg bg-gray-200"></div>
									</Table.Cell>
									<Table.Cell class="py-4 text-center">
										<div class="mx-auto h-6 w-6 animate-pulse rounded bg-gray-200"></div>
									</Table.Cell>
								</Table.Row>
							{/each}
						{:else if paginatedBarangs().length === 0}
							<Table.Row>
								<Table.Cell colspan={7} class="px-6 py-12 text-center">
									<Icon
										icon="mdi:package-variant-closed"
										width="48"
										height="48"
										class="mx-auto mb-4 text-gray-300"
									/>
									<h3 class="mb-2 text-lg font-medium text-gray-900">Tidak ada barang</h3>
									<p class="text-gray-500">
										Barang belum ditambahkan atau tidak sesuai dengan filter pencarian.
									</p>
								</Table.Cell>
							</Table.Row>
						{:else}
							{#each paginatedBarangs() as b}
								<Table.Row class="transition-colors hover:bg-gray-50">
									<Table.Cell class="whitespace-nowrap px-6 py-4 font-mono text-sm text-gray-900">
										{b.id_barang}
									</Table.Cell>
									<Table.Cell class="whitespace-nowrap py-4 text-sm font-medium text-gray-900">
										{b.nama_barang}
									</Table.Cell>
									<Table.Cell class="whitespace-nowrap py-4 text-sm text-gray-900">
										<span
											class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800"
										>
											{b.jumlah} unit
										</span>
									</Table.Cell>
									<Table.Cell class="whitespace-nowrap py-4 text-sm text-gray-900">
										<span
											class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
										>
											{b.kategori}
										</span>
									</Table.Cell>
									<Table.Cell class="max-w-xs py-4 text-sm text-gray-500">
										<p class="truncate" title={b.deskripsi}>
											{b.deskripsi || '-'}
										</p>
									</Table.Cell>
									<Table.Cell class="whitespace-nowrap py-4">
										{#if b.img}
											<img
												src={'data:image/png;base64,' + b.img}
												alt={b.nama_barang}
												class="h-12 w-12 rounded-lg border border-gray-200 object-cover"
											/>
										{:else}
											<div
												class="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-100"
											>
												<Icon icon="mdi:image" width="20" height="20" class="text-gray-400" />
											</div>
										{/if}
									</Table.Cell>
									<Table.Cell class="whitespace-nowrap py-4 text-center">
										<DropdownMenu.Root>
											<DropdownMenu.Trigger class="inline-flex rounded-md p-1 hover:bg-gray-100">
												<Icon
													icon="mdi:dots-vertical"
													width="20"
													height="20"
													class="text-gray-400"
												/>
											</DropdownMenu.Trigger>
											<DropdownMenu.Content>
												<DropdownMenu.Group>
													<DropdownMenu.Label>Aksi</DropdownMenu.Label>
													<DropdownMenu.Separator />
													<DropdownMenu.Item>
														<button
															class="w-full py-1 text-left text-sm text-blue-600 hover:text-blue-700"
															onclick={() =>
																dispatch('pageChange', { page: 'Update', id: b.id_barang })}
														>
															Edit Barang
														</button>
													</DropdownMenu.Item>
													<DropdownMenu.Item>
														<button
															class="w-full py-1 text-left text-sm text-red-600 hover:text-red-700"
															onclick={() => deleteBarang(b.id_barang)}
														>
															Hapus Barang
														</button>
													</DropdownMenu.Item>
												</DropdownMenu.Group>
											</DropdownMenu.Content>
										</DropdownMenu.Root>
									</Table.Cell>
								</Table.Row>
							{/each}
						{/if}
					</Table.Body>
				</Table.Root>
			</div>

			<!-- Pagination Footer -->
			{#if !loading && paginatedBarangs().length > 0}
				<div class="border-t border-gray-200 bg-white px-6 py-4">
					<div class="flex items-center justify-between">
						<div class="text-sm text-gray-700">
							Menampilkan <span class="font-medium">{(currentPage - 1) * perPage + 1}</span> hingga
							<span class="font-medium">{Math.min(currentPage * perPage, totalData())}</span> dari
							<span class="font-medium">{totalData()}</span> hasil
						</div>

						<Pagination.Root count={totalData()} {perPage} bind:page={currentPage}>
							{#snippet children({ pages, currentPage })}
								<nav class="relative z-0 inline-flex -space-x-px rounded-md shadow-sm">
									<Pagination.Item class="list-none">
										<Pagination.PrevButton
											class="relative inline-flex items-center rounded-l-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
										/>
									</Pagination.Item>
									{#each pages as page (page.key)}
										{#if page.type === 'ellipsis'}
											<Pagination.Item>
												<Pagination.Ellipsis
													class="relative inline-flex items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700"
												/>
											</Pagination.Item>
										{:else}
											<Pagination.Item class="list-none">
												<Pagination.Link
													{page}
													isActive={currentPage === page.value}
													class={`relative inline-flex items-center border px-4 py-2 text-sm font-medium ${
														currentPage === page.value
															? 'z-10 border-blue-500 bg-blue-50 text-blue-600'
															: 'border-gray-300 bg-white text-gray-500 hover:bg-gray-50'
													}`}
												>
													{page.value}
												</Pagination.Link>
											</Pagination.Item>
										{/if}
									{/each}
									<Pagination.Item>
										<Pagination.NextButton
											class="relative inline-flex items-center rounded-r-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
										/>
									</Pagination.Item>
								</nav>
							{/snippet}
						</Pagination.Root>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	li::marker {
		content: none; /* tidak menampilkan marker */
	}
</style>
