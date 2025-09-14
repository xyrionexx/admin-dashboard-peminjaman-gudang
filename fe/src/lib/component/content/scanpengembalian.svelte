<script lang="ts">
	import { Html5Qrcode } from 'html5-qrcode';

	let hasilScan: string = '';
	let scanner: Html5Qrcode | null = null;

	async function mulaiScan() {
		if (!scanner) {
			scanner = new Html5Qrcode('reader'); // div kamera
		}

		await scanner.start(
			{ facingMode: 'environment' }, // kamera belakang
			{ fps: 10, qrbox: 250 },
			(decodedText) => {
				// ✅ QR berhasil dibaca
				hasilScan = decodedText;
				console.log('QR terbaca:', decodedText);

				// Kirim ke server (pakai kode_detail)
				updateStatus(decodedText);

				// Stop scanner setelah dapat hasil
				scanner?.stop();
			},
			(errorMessage) => {
				console.log('Scan error:', errorMessage);
			}
		);
	}

	async function updateStatus(kode_detail: string) {
		try {
			const res = await fetch('http://127.0.0.1:8000/api/detail/detail-update-status/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ kode_detail })
			});

			const data = await res.json();
			alert(data.message);
		} catch (err) {
			alert('Gagal menghubungi server');
			console.error(err);
		}
	}
</script>

<div class="flex flex-col items-center space-y-4">
	<div id="reader" style="width:300px; height:300px; border:1px solid #ccc;"></div>
	<button on:click={mulaiScan} class="rounded bg-blue-500 px-4 py-2 text-white">
		Mulai Scan
	</button>
	<p>Hasil Scan: {hasilScan}</p>
</div>
